from datetime import datetime, timezone
from beanie import Document
from pydantic import EmailStr, Field


class User(Document):
    name: str
    email: EmailStr = Field(unique=True)
    password_hash: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "users"