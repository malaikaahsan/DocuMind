import os
import uuid
from beanie import PydanticObjectId

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)

from app.dependencies.auth import get_current_user
from app.models.document import DocumentRecord
from app.models.user import User
from app.models.document_chunk import DocumentChunk

from app.services.document_processor import process_pdf

router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)

UPLOAD_DIR = "uploads"

MAX_FILE_SIZE = 20 * 1024 * 1024

ALLOWED_CONTENT_TYPE = "application/pdf"

async def process_document(document_id: str):
    document = await DocumentRecord.get(
        PydanticObjectId(document_id)
    )

    if not document:
        return

    try:
        await DocumentChunk.find(
            DocumentChunk.document_id == document.id
        ).delete()
        result = process_pdf(document.storage_path)

        for chunk in result["chunks"]:
            document_chunk = DocumentChunk(
                document_id=document.id,
                user_id=document.user_id,
                chunk_index=chunk["chunk_index"],
                page_number=chunk["page_number"],
                text=chunk["text"],
            )

            await document_chunk.insert()

        document.page_count = result["page_count"]
        document.chunk_count = result["chunk_count"]
        document.status = "ready"

        await document.save()

    except Exception:
        document.status = "failed"
        await document.save()

@router.post("/upload")
async def upload_document(
     background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    if file.content_type != ALLOWED_CONTENT_TYPE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )

    file_extension = os.path.splitext(
        file.filename or ""
    )[1].lower()

    if file_extension != ".pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )

    file_data = await file.read()

    if len(file_data) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size must not exceed 20 MB"
        )

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    unique_name = f"{uuid.uuid4()}.pdf"

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_name
    )

    with open(file_path, "wb") as buffer:
        buffer.write(file_data)

    document = DocumentRecord(
        user_id=current_user.id,
        original_name=file.filename or "document.pdf",
        storage_path=file_path,
        status="processing",
    )

    await document.insert()

    background_tasks.add_task(
    process_document,
    str(document.id),
)

    return {
        "message": "Document uploaded successfully",
        "document": {
            "id": str(document.id),
            "original_name": document.original_name,
            "status": document.status,
        }
    }

@router.get("")
async def get_documents(
    current_user: User = Depends(get_current_user),
):
    documents = await DocumentRecord.find(
        DocumentRecord.user_id == current_user.id
    ).sort(
        -DocumentRecord.uploaded_at
    ).to_list()

    return {
        "documents": [
            {
                "id": str(document.id),
                "original_name": document.original_name,
                "status": document.status,
                "page_count": document.page_count,
                "chunk_count": document.chunk_count,
                "uploaded_at": document.uploaded_at,
            }
            for document in documents
        ]
    }

@router.get("/{document_id}")
async def get_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
):
    try:
        object_id = PydanticObjectId(document_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid document ID"
        )

    document = await DocumentRecord.get(object_id)

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    if document.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this document"
        )

    return {
        "id": str(document.id),
        "original_name": document.original_name,
        "status": document.status,
        "page_count": document.page_count,
        "chunk_count": document.chunk_count,
        "uploaded_at": document.uploaded_at,
    }

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
):
    try:
        object_id = PydanticObjectId(document_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid document ID"
        )

    document = await DocumentRecord.get(object_id)

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    if document.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this document"
        )

    if os.path.exists(document.storage_path):
        os.remove(document.storage_path)

    await document.delete()

    return {
        "message": "Document deleted successfully"
    }