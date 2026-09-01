from fastapi import APIRouter, HTTPException, status

from app.models.user import User
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
)
from app.services.security import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/register")
async def register_user(data: RegisterRequest):

    existing_user = await User.find_one(
        User.email == data.email
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered"
        )

    user = User(
        name=data.name.strip(),
        email=data.email,
        password_hash=hash_password(data.password)
    )

    await user.insert()

    return {
        "message": "User registered successfully"
    }


@router.post("/login")
async def login_user(data: LoginRequest):

    user = await User.find_one(
        User.email == data.email
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    password_valid = verify_password(
        data.password,
        user.password_hash
    )

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token(
        str(user.id)
    )

    return {
        "message": "Login successful",
        "token": token
    }