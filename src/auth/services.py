from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson.objectid import ObjectId

from .schemas import UserCreateModel
from .utils import generate_passwd_hash


class UserService:
    async def get_user_by_email(self, email: str, db: AsyncIOMotorDatabase):
        """Fetch a user by email."""
        return await db.users.find_one({"email": email})

    async def user_exists(self, email: str, db: AsyncIOMotorDatabase):
        """Check if a user exists by email."""
        return await self.get_user_by_email(email, db) is not None

    async def create_user(self, user_data: UserCreateModel, db: AsyncIOMotorDatabase):
        """Create a new user."""
        user_data_dict = user_data.model_dump()
        user_data_dict["fullname"] = user_data_dict["fullname"].title()
        user_data_dict["email"] = user_data_dict["email"].lower()
        user_data_dict["is_verified"] = True
        user_data_dict["password_hash"] = generate_passwd_hash(
            user_data_dict.pop("password")
        )
        user_data_dict["created_at"] = datetime.utcnow()

        result = await db.users.insert_one(user_data_dict)

        user_data_dict["_id"] = result.inserted_id  # Store inserted ID

        return user_data_dict

    async def update_user(
        self, user_id: str, user_data: dict, db: AsyncIOMotorDatabase
    ):
        """Update user details."""
        update_query = {"$set": user_data}
        await db.users.update_one({"_id": ObjectId(user_id)}, update_query)

        return await db.users.find_one({"_id": ObjectId(user_id)})
