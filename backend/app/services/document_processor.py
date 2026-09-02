import re
from pypdf import PdfReader

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")

    text = re.sub(r"[ \t]+", " ", text)

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

def extract_pdf_pages(file_path: str):
    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        text = clean_text(text)

        if not text:
            continue

        pages.append({
            "page_number": page_number,
            "text": text,
        })

    return pages

def chunk_text(
    text: str,
    chunk_size=CHUNK_SIZE,
    overlap=CHUNK_OVERLAP,
):
    if len(text) <= chunk_size:
        return [text]

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start += chunk_size - overlap

    return chunks

def create_chunks(pages):
    chunks = []

    chunk_index = 0

    for page in pages:
        page_number = page["page_number"]
        text = page["text"]

        page_chunks = chunk_text(text)

        for chunk in page_chunks:
            chunks.append({
                "chunk_index": chunk_index,
                "page_number": page_number,
                "text": chunk,
            })

            chunk_index += 1

    return chunks


def process_pdf(file_path: str):
    pages = extract_pdf_pages(file_path)

    chunks = create_chunks(pages)

    return {
        "pages": pages,
        "chunks": chunks,
        "page_count": len(pages),
        "chunk_count": len(chunks),
    }