# 🎵 TrackStack

A full-stack music analytics app that ingests song data from CSV, stores it in a database, and exposes search & stats APIs with a React frontend.

## ✨ Features
- **ETL Pipeline**: Load CSV data into a normalized database schema (Artists, Tracks, PlayHistory).
- **Backend (FastAPI + SQLAlchemy)**:
  - `/health` → health check
  - `/api/tracks/search` → search tracks/artists by name
  - `/api/stats/overview` → summary counts (artists, tracks)
- **Frontend (React + TypeScript + Vite)**:
  - Search UI for tracks/artists
  - Overview stats displayed on load
- **Database**: SQLite (easy local dev). Designed to swap to Postgres with Docker later.

## 🛠️ Tech Stack
- **Frontend**: React, TypeScript, Vite
- **Backend**: Python, FastAPI, SQLAlchemy
- **Database**: SQLite (local), Postgres (planned for Docker)
- **Other**: Pandas (for ETL), uvicorn (server)

## 🚀 Getting Started

### Prerequisites
- [Python 3.11+](https://www.python.org/)
- [Node.js (LTS)](https://nodejs.org/)
- [npm](https://www.npmjs.com/)

### Backend Setup
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt   # (or install fastapi, uvicorn, sqlalchemy, pandas manually)

# Run ETL to seed data
python -m app.seed_etl ..\data\sample_listens.csv

# Start API
uvicorn app.main:app --reload --port 8000
```
### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at http://localhost:5173

Backend runs at http://localhost:8000

### Author
Raghav Agarwal
- Computer Science @ Colorado State University
