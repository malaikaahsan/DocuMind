from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.search import SearchRequest, SearchResponse
from app.services.retrieval_service import search_similar_chunks


router = APIRouter(
    prefix="/api/search",
    tags=["Search"]
)


@router.post("", response_model=SearchResponse)
async def search_documents(
    data: SearchRequest,
    current_user: User = Depends(get_current_user),
):
    results = await search_similar_chunks(
        query=data.query,
        user_id=str(current_user.id),
        top_k=data.top_k,
        document_id=data.document_id,
    )

    return {
        "results": results
    }