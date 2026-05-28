import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("DATABASE_CONNECTION")
DB_NAME = os.getenv("DATABASE_NAME")

_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None

async def init_db():
    global _client, _db
    _client = AsyncIOMotorClient(MONGO_URL)
    _db = _client[DB_NAME]  # type: ignore
    # Verify connection
    await _client.admin.command("ping")
    print(f"✅ Connected to MongoDB: {DB_NAME}")

async def close_db():
    global _client
    if _client:
        _client.close()
        print("❌ MongoDB connection closed")

def get_db() -> AsyncIOMotorDatabase:
    if _db is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _db