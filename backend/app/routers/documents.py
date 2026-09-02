import os
import uuid
from beanie import PydanticObjectId

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)

from app.dependencies.auth import get_current_user
from app.models.document import DocumentRecord
from app.models.user import User

router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)

UPLOAD_DIR = "uploads"

MAX_FILE_SIZE = 20 * 1024 * 1024

ALLOWED_CONTENT_TYPE = "application/pdf"

@router.post("/upload")
async def upload_document(
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