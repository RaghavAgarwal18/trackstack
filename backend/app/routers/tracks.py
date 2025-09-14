from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Track, Artist

router = APIRouter()

@router.get("/search")
def search(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    stmt = (
        select(Track.id, Track.name, Artist.name.label("artist"), Track.album, Track.release_year)
        .join(Artist, Track.artist_id == Artist.id)
        .where((Track.name.ilike(f"%{q}%")) | (Artist.name.ilike(f"%{q}%")))
        .limit(50)
    )
    rows = db.execute(stmt).all()
    return [dict(id=i, name=n, artist=a, album=al, release_year=ry) for (i,n,a,al,ry) in rows]