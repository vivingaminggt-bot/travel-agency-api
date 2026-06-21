from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import models
from app.schemas import schemas
from app.services import cancellation_policy

router = APIRouter(prefix="/bookings", tags=["Bookings"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.BookingOut)
def create_booking(payload: schemas.BookingCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    trip = db.query(models.Trip).filter(models.Trip.id == payload.trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    available_seats = trip.total_seats - trip.booked_seats
    if available_seats < payload.num_travelers:
        raise HTTPException(status_code=400, detail="Not enough seats available")

    total_price = trip.price_per_person * payload.num_travelers

    booking = models.Booking(
        user_id=payload.user_id,
        trip_id=payload.trip_id,
        num_travelers=payload.num_travelers,
        total_price=total_price,
        status="confirmed",
    )
    trip.booked_seats += payload.num_travelers

    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.get("/{booking_id}", response_model=schemas.BookingOut)
def get_booking(booking_id: str, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.post("/{booking_id}/cancel")
def cancel_booking(booking_id: str, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.status == "cancelled":
        raise HTTPException(status_code=400, detail="Booking already cancelled")

    trip = db.query(models.Trip).filter(models.Trip.id == booking.trip_id).first()

    days_before = cancellation_policy.days_until(trip.start_date)
    refund_pct = cancellation_policy.compute_refund_percentage(days_before)
    refund_amount = round(booking.total_price * refund_pct, 2)

    booking.status = "cancelled"
    booking.cancelled_at = datetime.utcnow()
    trip.booked_seats -= booking.num_travelers

    db.commit()

    return {
        "booking_id": booking.id,
        "status": booking.status,
        "days_before_trip": days_before,
        "refund_percentage": refund_pct,
       "refund_amount": refund_amount,
    }