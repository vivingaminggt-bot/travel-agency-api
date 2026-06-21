import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, Float, Text, ForeignKey
from app.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    loyalty_points = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class Destination(Base):
    __tablename__ = "destinations"

    id = Column(String, primary_key=True, default=gen_uuid)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    popularity_score = Column(Float, default=0.0)


class Trip(Base):
    __tablename__ = "trips"

    id = Column(String, primary_key=True, default=gen_uuid)
    title = Column(String, nullable=False)
    destination_id = Column(String, ForeignKey("destinations.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    price_per_person = Column(Float, nullable=False)
    total_seats = Column(Integer, nullable=False)
    booked_seats = Column(Integer, default=0)


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    trip_id = Column(String, ForeignKey("trips.id"), nullable=False)
    num_travelers = Column(Integer, default=1)
    total_price = Column(Float, nullable=False)
    status = Column(String, default="confirmed")
    booked_at = Column(DateTime, default=datetime.utcnow)
    cancelled_at = Column(DateTime, nullable=True)