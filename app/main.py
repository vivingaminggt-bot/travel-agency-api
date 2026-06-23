from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine, SessionLocal
from app.models import models
from app.routers import users, destinations, trips, bookings, ai

Base.metadata.create_all(bind=engine)


def seed_data():
    db = SessionLocal()
    try:
        if db.query(models.Trip).count() > 0:
            return
        paris = models.Destination(city="Paris", country="France", description="City of lights")
        bali = models.Destination(city="Bali", country="Indonesia", description="Tropical paradise")
        tokyo = models.Destination(city="Tokyo", country="Japan", description="Futuristic city")
        db.add_all([paris, bali, tokyo])
        db.commit()
        from datetime import datetime, timedelta
        now = datetime.utcnow()
        db.add_all([
            models.Trip(title="Romantic Paris Getaway", destination_id=paris.id,
                start_date=now+timedelta(days=80), end_date=now+timedelta(days=84),
                price_per_person=1200, total_seats=15),
            models.Trip(title="Bali Beach Escape", destination_id=bali.id,
                start_date=now+timedelta(days=100), end_date=now+timedelta(days=107),
                price_per_person=850, total_seats=20),
            models.Trip(title="Tokyo Explorer", destination_id=tokyo.id,
                start_date=now+timedelta(days=130), end_date=now+timedelta(days=137),
                price_per_person=1500, total_seats=18),
        ])
        db.commit()
    finally:
        db.close()


seed_data()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(destinations.router)
app.include_router(trips.router)
app.include_router(bookings.router)
app.include_router(ai.router)


@app.get("/")
def root():
    return {"message": "Travel Agency API is alive"}