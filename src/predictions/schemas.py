from datetime import datetime
import uuid
from pydantic import BaseModel
from typing import List, Optional


class PredictionResponseModel(BaseModel):
    id: str
    image: str
    disease: str
    confidence: float
    date: datetime
    plant: str
    description: str
    treatments: List[str]


class PredictionRequestModel(BaseModel):
    image_url: str
    user_id: uuid.UUID
