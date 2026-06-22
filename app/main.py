from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import models
from app.routers import users, destinations, trips, bookings, ai

Base.metadata.create_all(bind=engine)

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