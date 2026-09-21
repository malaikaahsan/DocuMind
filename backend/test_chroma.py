# from app.services.vector_store import get_collection

# collection = get_collection()

# collection.delete(
#     ids=["test-1", "test-2"]
# )

# print("Test vectors deleted")
# print("Total vectors:", collection.count())


from app.services.vector_store import get_collection

collection = get_collection()

print("Collection name:", collection.name)
print("Total vectors:", collection.count())