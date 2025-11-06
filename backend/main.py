# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Base
from auth import router as auth_router
from notes import router as notes_router

# Create FastAPI app
app = FastAPI()

# --- CORS Setup ---
origins = [
    "http://localhost:3000",  # frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # allow requests from this origin
    allow_credentials=True,
    allow_methods=["*"],        # allow POST, GET, PUT, DELETE, OPTIONS
    allow_headers=["*"],        # allow Authorization, Content-Type, etc.
)

# --- Database tables ---
Base.metadata.create_all(bind=engine)

# --- Include routers ---
app.include_router(auth_router)
app.include_router(notes_router)
