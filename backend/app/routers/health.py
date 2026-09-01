from fastapi import APIRouter

router = APIRouter(
    prefix="/api",
    tags=["System"],
)


@router.get("/health")
async def health_check():
    return {
        "status": "success",
        "message": "DocuMind API is running",
    }