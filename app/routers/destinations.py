from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import models
from app.schemas import schemas

router = APIRouter(prefix="/destinations", tags=["Destinations"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.DestinationOut)
def create_destination(payload: schemas.DestinationCreate, db: Session = Depends(get_db)):
    destination = models.Destination(
        city=payload.city,
        country=payload.country,
        description=payload.description,
    )
    db.add(destination)
    db.commit()
    db.refresh(destination)
    return destination


@router.get("/", response_model=list[schemas.DestinationOut])
def list_destinations(db: Session = Depends(get_db)):
    return db.query(models.Destination).all()