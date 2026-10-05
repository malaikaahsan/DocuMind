from app.services.embedding_service import generate_embeddings
from app.services.vector_store import get_collection
from beanie import PydanticObjectId

from app.models.document import DocumentRecord


async def search_similar_chunks(
    query: str,
    user_id: str,
    top_k: int = 5,
    document_id: str | None = None,
):
    query_embedding = generate_embeddings([query])[0]

    collection = get_collection()

    where = {
        "user_id": user_id
    }

    if document_id:
        where = {
            "$and": [
                {"user_id": user_id},
                {"document_id": document_id},
            ]
        }

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where,
    )

    formatted_results = []

    ids = results.get("ids", [[]])[0]
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    document_ids = set()

    for metadata in metadatas:
        document_ids.add(metadata["document_id"])

    document_names = {}

    for current_document_id in document_ids:
        document = await DocumentRecord.get(
            PydanticObjectId(current_document_id)
        )

        if document:
            document_names[current_document_id] = (
                document.original_name
            )

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        current_document_id = metadata["document_id"]

        formatted_results.append({
            "document_id": current_document_id,
            "document_name": document_names.get(
                current_document_id,
                "Unknown document"
            ),
            "page_number": metadata["page_number"],
            "chunk_index": metadata["chunk_index"],
            "text": document,
            "distance": distance,
        })

    return formatted_results