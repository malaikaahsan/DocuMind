from app.services.document_processor import process_pdf


result = process_pdf("uploads/26a3f172-0468-4c78-9047-5660f8baced4.pdf")

print("Pages:", result["page_count"])
print("Chunks:", result["chunk_count"])


for chunk in result["chunks"][:3]:
    print("\n--- CHUNK ---")
    print("Page:", chunk["page_number"])
    print(chunk["text"])