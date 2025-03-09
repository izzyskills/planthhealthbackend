from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from src.config import Config
from gridfs import GridFS


# Initialize Async MongoDB Client
client = AsyncIOMotorClient(Config.DATABASE_URL)
db = client.get_database()  # Adjust if needed (e.g., `client["your_db_name"]`)

# GridFS for image storage
fs = AsyncIOMotorGridFSBucket(db)


async def init_db():
    """MongoDB does not require explicit schema creation like SQL databases."""
    print("MongoDB initialized")


async def get_session():
    """Yield the MongoDB database connection."""
    yield db
