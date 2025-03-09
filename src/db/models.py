from bson.objectid import ObjectId
from datetime import datetime
from .main import db, fs


# User Model
class User:
    def __init__(self, fullname, email, password_hash, is_verified=False):
        self.fullname = fullname
        self.email = email
        self.password_hash = password_hash
        self.is_verified = is_verified
        self.created_at = datetime.utcnow()

    async def save(self):
        result = await db.users.insert_one(self.__dict__)  # ✅ Async insert
        return result.inserted_id


# Disease Model
class Disease:
    def __init__(self, name, description, treatments, disease_image, plant):
        self.name = name
        self.description = description
        self.treatments = treatments
        self.disease_image = disease_image  # Store image_id if needed
        self.plant = plant
        self.created_at = datetime.utcnow()

    async def save(self):
        result = await db.diseases.insert_one(self.__dict__)  # ✅ Async insert
        return result.inserted_id


# Prediction Model (with Image Storage)
class Prediction:
    def __init__(self, user_id, image_data, disease_id, prediction, confidence):
        self.user_id = ObjectId(user_id)
        self.disease_id = ObjectId(disease_id)
        self.prediction = prediction
        self.confidence = confidence
        self.created_at = datetime.utcnow()

    async def save(self, image_data):
        self.image_id = await fs.upload_from_stream(
            "prediction_image", image_data
        )  # ✅ Async GridFS
        result = await db.predictions.insert_one(self.__dict__)  # ✅ Async insert
        return result.inserted_id

    @staticmethod
    async def get_image(image_id):
        """Retrieve image from GridFS (Async)"""
        image_stream = await fs.open_download_stream(
            ObjectId(image_id)
        )  # ✅ Async GridFS retrieval
        return await image_stream.read()
