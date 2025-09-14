from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db

app = FastAPI(title="TrackStack API", version="0.1.0")

# Allow your React dev server to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

from .routers import tracks
app.include_router(tracks.router, prefix="/api/tracks", tags=["tracks"])

from .routers import stats
app.include_router(stats.router, prefix="/api/stats", tags=["stats"])