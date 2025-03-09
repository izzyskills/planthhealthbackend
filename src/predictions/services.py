from datetime import datetime
from typing import Dict, List, Optional, Tuple
import uuid
from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import array_agg
from sqlmodel import and_, desc, func, or_, select, case, distinct
from sqlmodel.sql.expression import Select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import User, Disease, Prediction


class PredictionService:
    async def get_prediction_by_id(
        self, prediction_id: uuid.UUID, session: AsyncSession
    ):
        statement = select(Prediction).where(Prediction.id == prediction_id)

        result = await session.exec(statement)

        prediction = result.first()

        return prediction

    async def get_predictions_by_user_id(
        self, user_id: uuid.UUID, session: AsyncSession
    ):
        statement = select(Prediction).where(Prediction.user_id == user_id)

        result = await session.exec(statement)

        predictions = result.all()

        return predictions

    async def get_predictions_by_disease_id(
        self, disease_id: uuid.UUID, session: AsyncSession
    ):
        statement = select(Prediction).where(Prediction.disease_id == disease_id)

        result = await session.exec(statement)

        predictions = result.all()

        return predictions

    async def get_predictions_by_user_and_disease(
        self, user_id: uuid.UUID, disease_id: uuid.UUID, session: AsyncSession
    ):
        statement = select(Prediction).where(
            and_(Prediction.user_id == user_id, Prediction.disease_id == disease_id)
        )

        result = await session.exec(statement)

        predictions = result.all()

        return predictions

    async def get_all_predictions(self, session: AsyncSession):
        statement = select(Prediction)

        result = await session.exec(statement)

        predictions = result.all()

        return predictions

    async def get_user_last_five_predictions(
        self, user_id: uuid.UUID, session: AsyncSession
    ):
        statement = (
            select(Prediction)
            .where(Prediction.user_id == user_id)
            .order_by(desc(Prediction.created_at))
            .limit(5)
        )

        result = await session.exec(statement)

        predictions = result.all()

        return predictions

    async def create_prediction(
        self, prediction_data: Dict, session: AsyncSession
    ) -> Prediction:
        new_prediction = Prediction(**prediction_data)

        session.add(new_prediction)

        await session.commit()

        return new_prediction

    async def update_prediction(
        self, prediction: Prediction, prediction_data: Dict, session: AsyncSession
    ) -> Prediction:
        for k, v in prediction_data.items():
            setattr(prediction, k, v)

        await session.commit()

        return prediction

    async def delete_prediction(self, prediction_id: uuid.UUID, session: AsyncSession):
        statement = select(Prediction).where(Prediction.id == prediction_id)

        result = await session.exec(statement)

        prediction = result.first()

        if prediction is None:
            raise HTTPException(status_code=404, detail="Prediction not found")

        await session.delete(prediction)

        await session.commit()

        return prediction
