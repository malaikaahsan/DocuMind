from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)

database = client[settings.DATABASE_NAME]

async def connect_to_mongodb():
    await client.admin.command("ping")
    print("MongoDB connected successfully")


async def close_mongodb_connection():
    client.close()
    print("MongoDB connection closed")