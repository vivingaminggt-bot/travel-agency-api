from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import SessionLocal
from app.models import models
from app.services import llm_service

router = APIRouter(prefix="/ai", tags=["AI"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ChatRequest(BaseModel):
    user_id: str
    message: str


class RecommendRequest(BaseModel):
    preferences: str


@router.post("/chat")
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reply = llm_service.chat_reply([], payload.message)

    return {
        "user_id": payload.user_id,
        "message": payload.message,
        "reply": reply,
    }


@router.post("/recommend")
def recommend(payload: RecommendRequest, db: Session = Depends(get_db)):
    trips = db.query(models.Trip).all()

    available_trips = [
        {
            "title": t.title,
            "city": db.query(models.Destination).filter(
                models.Destination.id == t.destination_id
            ).first().city,
            "country": db.query(models.Destination).filter(
                models.Destination.id == t.destination_id
            ).first().country,
            "price_per_person": t.price_per_person,
            "available_seats": t.total_seats - t.booked_seats,
        }
        for t in trips
    ]

    recommendation = llm_service.generate_recommendation(
        payload.preferences,
        available_trips
    )

    return {
        "preferences": payload.preferences,
        "recommendation": recommendation,
    }