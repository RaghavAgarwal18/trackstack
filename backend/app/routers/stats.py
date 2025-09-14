from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Artist, Track

router = APIRouter()

@router.get("/overview")
def overview(db: Session = Depends(get_db)):
    artists = db.scalar(select(func.count(Artist.id))) or 0
    tracks  = db.scalar(select(func.count(Track.id))) or 0
    return {"artists": artists, "tracks": tracks}