from datetime import datetime

from pydantic import BaseModel

class DocumentResponse(BaseModel):
    id: str
    original_name: str
    status: str
    page_count: int
    chunk_count: int
    uploaded_at: datetime