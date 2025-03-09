from bson import ObjectId
import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, model_validator


class UserCreateModel(BaseModel):
    fullname: str = Field(max_length=25)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "johndoe123@co.com",
                "fullname": "John Doe",
                "password": "testpass123",
            }
        }
    }


class UserResponseModel(BaseModel):
    id: str
    fullname: str
    email: str
    is_verified: bool
    created_at: datetime

    @model_validator(mode="before")
    def serialize_objectid(cls, values):
        if "_id" in values:
            values["id"] = str(values["_id"])  # Convert ObjectId to string
            del values["_id"]
        return values

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    uid: uuid.UUID
    email: str
    fullname: str
    password_hash: str = Field(exclude=True)
    created_at: datetime


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


class EmailModel(BaseModel):
    addresses: List[str]


class PasswordResetRequestModel(BaseModel):
    email: str


class PasswordResetConfirmModel(BaseModel):
    new_password: str
    confirm_new_password: str
