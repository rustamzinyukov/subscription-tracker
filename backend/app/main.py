# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

# Import our modules
from .core.database import get_db, create_tables
from .core.auth import auth_manager, get_current_user
from .models.database import User

load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Subscription Tracker API",
    description="Multi-platform subscription management service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    from .core.database import drop_tables, create_tables
    # Drop and recreate tables to ensure schema is up to date
    drop_tables()
    create_tables()

# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "Subscription Tracker API",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Subscription Tracker API",
        "docs": "/docs",
        "health": "/health"
    }

# Import and include routers
from .routers import auth, subscriptions, analytics, telegram

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(subscriptions.router, prefix="/api/v1/subscriptions", tags=["Subscriptions"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(telegram.router, prefix="/api/v1/telegram", tags=["Telegram"])