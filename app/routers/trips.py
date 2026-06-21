from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import models
from app.schemas import schemas

router = APIRouter(prefix="/trips", tags=["Trips"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.TripOut)
def create_trip(payload: schemas.TripCreate, db: Session = Depends(get_db)):
    destination = db.query(models.Destination).filter(
        models.Destination.id == payload.destination_id
    ).first()
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")

    trip = models.Trip(
        title=payload.title,
        destination_id=payload.destination_id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        price_per_person=payload.price_per_person,
        total_seats=payload.total_seats,
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


@router.get("/", response_model=list[schemas.TripOut])
def list_trips(db: Session = Depends(get_db)):
    return db.query(models.Trip).all()