import asyncio
import os
from typing import List, Optional, BinaryIO
import uuid
import numpy as np
import tensorflow as tf
from io import BytesIO
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.param_functions import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from bson.objectid import ObjectId
from datetime import datetime

from src.auth.dependencies import (
    AccessTokenBearer,
)
from src.db.main import get_session, db
from src.db.models import Prediction
from .schemas import PredictionResponseModel

# Initialize the router
prediction_router = APIRouter()

# Get the directory of the current file (router.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the TensorFlow model using absolute path
model_path = os.path.join(current_dir, "my_model.h5")
try:
    model = tf.keras.models.load_model(model_path)
    print(f"Successfully loaded model from {model_path}")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    # We'll raise an exception during the first API call if the model isn't loaded
    model = None

# Define class names matching those used to seed the database
class_names = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
]


# Helper function to preprocess image for model prediction
async def preprocess_image(file: UploadFile):
    """Preprocess uploaded image for model prediction"""
    # Read file content
    contents = await file.read()

    # Create a BytesIO object for TensorFlow to read from
    img_bytes = BytesIO(contents)

    # Use TensorFlow to decode the image
    img = tf.io.decode_image(contents)
    img = tf.image.resize(img, (224, 224))
    img = tf.expand_dims(img, axis=0) / 255.0  # Normalize to [0,1]

    # Reset file pointer for future reads
    await file.seek(0)

    return img, contents


@prediction_router.post("/", response_model=PredictionResponseModel)
async def predict_disease(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    token_data: dict = Depends(AccessTokenBearer()),
):
    """
    Predict plant disease based on uploaded image
    """
    if model is None:
        raise HTTPException(
            status_code=500, detail="Model not loaded. Check server logs."
        )

    user_id = token_data["user"]["user_id"]

    # Check file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Preprocess the image
        img, image_data = await preprocess_image(file)

        # Make prediction (run in a thread pool to avoid blocking)
        predictions = await asyncio.to_thread(model.predict, img)
        predictions = predictions[0]

        pred_class_idx = np.argmax(predictions)
        pred_class_name = class_names[pred_class_idx]
        confidence = float(predictions[pred_class_idx])

        # Get the disease information from the database
        disease = await db.diseases.find_one({"disease_image": pred_class_name})

        if not disease:
            raise HTTPException(
                status_code=404,
                detail=f"Disease information not found for {pred_class_name}",
            )

        # Create a prediction record
        prediction = Prediction(
            user_id=user_id,
            disease_id=disease["_id"],
            prediction=pred_class_name,
            confidence=confidence,
            image_data=image_data,
        )

        # Save prediction with image
        prediction_id = await prediction.save(image_data)

        # Format the response
        return PredictionResponseModel(
            id=str(prediction_id),  # Convert ObjectId to string
            image=file.filename,
            disease=disease["name"],
            confidence=confidence,
            date=datetime.utcnow(),
            plant=disease["plant"],
            description=disease["description"],
            treatments=disease["treatments"],
        )

    except Exception as e:
        import traceback

        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@prediction_router.get("/predictions", response_model=List[PredictionResponseModel])
async def get_predictions(
    session: AsyncSession = Depends(get_session),
    token_data: dict = Depends(AccessTokenBearer()),
):
    """
    Get all predictions for the authenticated user
    """
    user_id = token_data["user"]["user_id"]

    try:
        # Find all predictions for this user
        user_predictions = []
        cursor = db.predictions.find({"user_id": ObjectId(user_id)}).sort(
            "created_at", -1
        )

        async for pred in cursor:
            # Get the associated disease information
            disease = await db.diseases.find_one({"_id": pred["disease_id"]})

            if disease:
                user_predictions.append(
                    PredictionResponseModel(
                        id=str(pred["_id"]),  # Convert ObjectId to string
                        image=str(pred["image_id"]),  # Use the GridFS image ID
                        disease=disease["name"],
                        confidence=pred["confidence"],
                        date=pred["created_at"],
                        plant=disease["plant"],
                        description=disease["description"],
                        treatments=disease["treatments"],
                    )
                )

        return user_predictions

    except Exception as e:
        import traceback

        print(traceback.format_exc())
        raise HTTPException(
            status_code=500, detail=f"Error retrieving predictions: {str(e)}"
        )


@prediction_router.get("/{prediction_id}/image")
async def get_prediction_image(
    prediction_id: str,
):
    """
    Get the image for a specific prediction
    """

    try:
        # Find the prediction
        prediction = await db.predictions.find_one({"_id": ObjectId(prediction_id)})

        if not prediction:
            raise HTTPException(status_code=404, detail="Prediction not found")

        print("move")
        # Get the image from GridFS
        image_data = await Prediction.get_image(prediction["image_id"])

        # Return the image
        from fastapi.responses import Response

        return Response(content=image_data, media_type="image/jpeg")

    except Exception as e:
        import traceback

        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving image: {str(e)}")
