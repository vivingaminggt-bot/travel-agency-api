from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None


class UserOut(BaseModel):
    id: str
    name: str
    email: str
    phone: str | None
    loyalty_points: int

    class Config:
        from_attributes = True


class DestinationCreate(BaseModel):
    city: str
    country: str
    description: str | None = None


class DestinationOut(BaseModel):
    id: str
    city: str
    country: str
    description: str | None
    popularity_score: float

    class Config:
        from_attributes = True


class TripCreate(BaseModel):
    title: str
    destination_id: str
    start_date: datetime
    end_date: datetime
    price_per_person: float
    total_seats: int


class TripOut(BaseModel):
    id: str
    title: str
    destination_id: str
    start_date: datetime
    end_date: datetime
    price_per_person: float
    total_seats: int
    booked_seats: int

    class Config:
        from_attributes = True


class BookingCreate(BaseModel):
    user_id: str
    trip_id: str
    num_travelers: int = 1


class BookingOut(BaseModel):
    id: str
    user_id: str
    trip_id: str
    num_travelers: int
    total_price: float
    status: str
    booked_at: datetime
    cancelled_at: datetime | None

    class Config:
        from_attributes = True