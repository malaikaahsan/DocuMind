from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/api",
    tags=["Authentication"]
)


@router.get("/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": str(current_user.id),
        "name": current_user.name,
        "email": current_user.email
    }