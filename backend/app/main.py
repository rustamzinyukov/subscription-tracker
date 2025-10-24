# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import os
import time
from dotenv import load_dotenv

# Import our modules
from .core.database import get_db, create_tables
from .core.auth import auth_manager, get_current_user
from .models.database import User

# Import migration function
def run_migration():
    """Run database migration on startup"""
    try:
        from alembic.config import Config
        from alembic import command
        import os
        
        print("🔄 Running database migration...")
        
        # Change to the backend directory where alembic.ini is located
        os.chdir("/app")
        print(f"📁 Current directory: {os.getcwd()}")
        print(f"📁 Alembic.ini exists: {os.path.exists('alembic.ini')}")
        print(f"📁 Files in /app: {os.listdir('/app')}")
        print(f"📁 Alembic directory exists: {os.path.exists('alembic')}")
        if os.path.exists('alembic'):
            print(f"📁 Files in alembic: {os.listdir('alembic')}")
        
        alembic_cfg = Config("alembic.ini")
        print(f"📁 Alembic config loaded: {alembic_cfg}")
        
        command.upgrade(alembic_cfg, "head")
        print("✅ Database migration completed!")
    except Exception as e:
        print(f"⚠️ Migration failed (this might be normal for first run): {e}")
        print(f"⚠️ Error details: {str(e)}")
        # Continue anyway - tables will be created by create_tables()

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
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,https://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    print(f"📥 Incoming request: {request.method} {request.url.path}")
    print(f"🔑 Authorization header: {request.headers.get('authorization', 'Not present')}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    print(f"📤 Response: {response.status_code} (took {process_time:.2f}s)")
    
    return response

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    from .core.database import create_tables
    # Run migration first
    run_migration()
    
    # Create tables if they don't exist
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