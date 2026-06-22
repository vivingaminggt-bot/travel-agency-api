import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from groq import Groq

from app.database import get_db
from app.models import models

router = APIRouter(prefix="/ai", tags=["AI"])

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


class ChatRequest(BaseModel):
    user_id: str
    message: str


class RecommendRequest(BaseModel):
    preferences: str


@router.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == req.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a friendly, helpful AI travel assistant for an online travel agency. "
                                "Answer questions about destinations, packing, best time to travel, and help "
                                "users decide on trips. Keep replies short and conversational (2-4 sentences).",
                },
                {"role": "user", "content": req.message},
            ],
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        reply = "Sorry, I'm having trouble responding right now. Please try again in a moment."

    return {"reply": reply}


@router.post("/recommend")
def recommend(req: RecommendRequest, db: Session = Depends(get_db)):
    trips = db.query(models.Trip).all()
    destinations = {d.id: d for d in db.query(models.Destination).all()}

    if not trips:
        return {"recommendation": "We don't have any trips available right now. Please check back soon!"}

    trip_lines = []
    for t in trips:
        dest = destinations.get(t.destination_id)
        location = f"{dest.city}, {dest.country}" if dest else "Unknown"
        available = t.total_seats - t.booked_seats
        trip_lines.append(
            f"- {t.title} in {location}: ${t.price_per_person}/person, "
            f"{t.start_date.date()} to {t.end_date.date()}, {available} seats left"
        )
    inventory_text = "\n".join(trip_lines)

    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a travel recommendation assistant. You will be given a list of real "
                                "available trips and a user's preferences. Recommend the best matching trip(s) "
                                "from the list ONLY (never invent trips). Explain briefly why they fit. "
                                "Keep it to 3-5 sentences, friendly and concise.",
                },
                {
                    "role": "user",
                    "content": f"Available trips:\n{inventory_text}\n\nUser preferences: {req.preferences}",
                },
            ],
        )
        recommendation = completion.choices[0].message.content
    except Exception as e:
        recommendation = "Sorry, I couldn't generate a recommendation right now. Please try again shortly."

    return {"recommendation": recommendation}