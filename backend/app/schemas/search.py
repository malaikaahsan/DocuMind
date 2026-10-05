from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=10)
    document_id: str | None = None


class SearchResult(BaseModel):
    document_id: str
    document_name: str
    page_number: int
    chunk_index: int
    text: str
    distance: float


class SearchResponse(BaseModel):
    results: list[SearchResult]