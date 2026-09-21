import chromadb


client = chromadb.PersistentClient(
    path="chroma_db"
)


def get_collection():
    return client.get_or_create_collection(
        name="documind_documents"
    )

def add_chunks(
    ids,
    documents,
    embeddings,
    metadatas,
):
    collection = get_collection()

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

def delete_document_chunks(document_id: str):
    collection = get_collection()

    collection.delete(
        where={
            "document_id": document_id
        }
    )