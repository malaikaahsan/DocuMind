from datetime import datetime, timezone

from pydantic import Field
from beanie import Document, PydanticObjectId

class DocumentRecord(Document):
    user_id: PydanticObjectId
    original_name: str
    storage_path: str

    status: str = "processing"

    page_count: int = 0
    chunk_count: int = 0

    chroma_collection_id: str = ""

    uploaded_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "documents"