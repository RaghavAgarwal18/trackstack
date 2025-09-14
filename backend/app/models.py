from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime
from .database import Base
from datetime import datetime  # 👈 add this import

class Artist(Base):
    __tablename__ = "artists"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)

class Track(Base):
    __tablename__ = "tracks"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id"))
    album: Mapped[str | None] = mapped_column(String(255), nullable=True)
    release_year: Mapped[int | None] = mapped_column(nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(nullable=True)
    artist = relationship("Artist")

class PlayHistory(Base):
    __tablename__ = "play_history"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    track_id: Mapped[int] = mapped_column(primary_key=True)
    played_at: Mapped[datetime] = mapped_column(DateTime, primary_key=True) 