from app.services.retrieval_service import search_similar_chunks


query = "What is this document about?"

results = search_similar_chunks(
    query=query,
    user_id="6a97085098c1b1b48efccd7b",
    top_k=5,
)

print("IDs:")
print(results["ids"])

print("\nDocuments:")
print(results["documents"])

print("\nMetadatas:")
print(results["metadatas"])

print("\nDistances:")
print(results["distances"])