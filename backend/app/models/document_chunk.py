from datetime import datetime, timezone

from beanie import Document, PydanticObjectId
from pydantic import Field


class DocumentChunk(Document):
    document_id: PydanticObjectId
    user_id: PydanticObjectId

    chunk_index: int
    page_number: int
    text: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "document_chunks"