import asyncio
from app.database.connection import connect_to_mongodb

from app.models.document import DocumentRecord
from app.models.document_chunk import DocumentChunk
from app.services.vector_store import get_collection


async def main():
    await connect_to_mongodb()
    documents = await DocumentRecord.find_all().to_list()

    collection = get_collection()

    print("Total Chroma vectors:", collection.count())
    print("Total documents:", len(documents))

    for document in documents:
        mongo_chunks = await DocumentChunk.find(
            DocumentChunk.document_id == document.id
        ).to_list()

        chroma_results = collection.get(
            where={
                "document_id": str(document.id)
            },
            include=["metadatas"]
        )

        chroma_count = len(chroma_results["ids"])

        print("\nDocument:", document.original_name)
        print("Document ID:", document.id)
        print("MongoDB chunks:", len(mongo_chunks))
        print("Chroma vectors:", chroma_count)
        print("Document status:", document.status)

        if len(mongo_chunks) == chroma_count:
            print("✓ Consistent")
        else:
            print("✗ Mismatch")


if __name__ == "__main__":
    asyncio.run(main())