import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import SessionLocal, init_db          # <- single dot
from .models import Artist, Track, PlayHistory       # <- single dot
from datetime import datetime

def upsert_artist(db: Session, name: str) -> int:
    name = (name or "Unknown Artist").strip()
    row = db.execute(select(Artist).where(Artist.name == name)).scalar_one_or_none()
    if row: return row.id
    a = Artist(name=name); db.add(a); db.flush(); return a.id

def upsert_track(db: Session, name: str, artist_id: int, album=None, year=None, duration_ms=None) -> int:
    row = db.execute(select(Track).where(Track.name==name, Track.artist_id==artist_id)).scalar_one_or_none()
    if row: return row.id
    t = Track(name=name, artist_id=artist_id, album=album, release_year=year, duration_ms=duration_ms)
    db.add(t); db.flush(); return t.id

def main(csv_path: str):
    init_db()
    df = pd.read_csv(csv_path)
    db = SessionLocal()
    try:
        for _, r in df.iterrows():
            artist_id = upsert_artist(db, str(r.get("artist", "")))
            track_id = upsert_track(
                db, str(r.get("track","")), artist_id,
                album=r.get("album"),
                year=int(r["year"]) if "year" in r and pd.notna(r["year"]) else None,
                duration_ms=int(r["duration_ms"]) if "duration_ms" in r and pd.notna(r["duration_ms"]) else None
            )
            if "played_at" in r and pd.notna(r["played_at"]):
                played_at = pd.to_datetime(r["played_at"]).to_pydatetime()
                ph = PlayHistory(user_id=1, track_id=track_id, played_at=played_at)
                db.merge(ph)
        db.commit()
        print("✅ ETL done")
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m app.seed_etl ../data/sample_listens.csv")
        raise SystemExit(1)
    main(sys.argv[1])