from pymongo import AsyncMongoClient
from beanie import init_beanie

from app.config import settings
from app.models.user import User


client = AsyncMongoClient(settings.MONGO_URI)

database = client[settings.DATABASE_NAME]


async def connect_to_mongodb():
    await client.admin.command("ping")

    await init_beanie(
        database=database,
        document_models=[
            User,
        ],
    )

    print("MongoDB connected successfully")


async def close_mongodb_connection():
    await client.close()
    print("MongoDB connection closed")