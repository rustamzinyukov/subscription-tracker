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
        
        # Check database connection
        from .core.database import get_database_url
        db_url = get_database_url()
        print(f"🔗 Database URL: {db_url[:50]}..." if len(db_url) > 50 else f"🔗 Database URL: {db_url}")
        
        # Test database connection
        try:
            from sqlalchemy import create_engine, text
            engine = create_engine(db_url)
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print("✅ Database connection test successful!")
                
                # Check if subscriptions table exists
                result = conn.execute(text("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'subscriptions'"))
                table_exists = result.scalar()
                print(f"📊 Subscriptions table exists: {table_exists > 0}")
                
                if table_exists > 0:
                    # Check current columns
                    result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'subscriptions' ORDER BY ordinal_position"))
                    columns = [row[0] for row in result.fetchall()]
                    print(f"📊 Current columns: {columns}")
                    
                    # Check if advanced columns already exist
                    advanced_columns = ['subscription_type', 'has_trial', 'trial_start_date', 'interval_unit']
                    existing_advanced = [col for col in advanced_columns if col in columns]
                    print(f"📊 Advanced columns already exist: {existing_advanced}")
                    
        except Exception as e:
            print(f"❌ Database connection test failed: {e}")
            return
        
        # Change to the root directory where alembic.ini is located
        os.chdir("/app")
        print(f"📁 Current directory: {os.getcwd()}")
        print(f"📁 Alembic.ini exists: {os.path.exists('alembic.ini')}")
        print(f"📁 Files in /app: {os.listdir('/app')}")
        print(f"📁 Alembic directory exists: {os.path.exists('alembic')}")
        if os.path.exists('alembic'):
            print(f"📁 Files in alembic: {os.listdir('alembic')}")
            if os.path.exists('alembic/versions'):
                print(f"📁 Files in alembic/versions: {os.listdir('alembic/versions')}")
        
        alembic_cfg = Config("alembic.ini")
        print(f"📁 Alembic config loaded: {alembic_cfg}")
        
        print("🚀 Starting Alembic upgrade command...")
        
        # Add timeout and more detailed logging
        import signal
        import time
        
        def timeout_handler(signum, frame):
            raise TimeoutError("Migration timed out after 30 seconds")
        
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(30)  # 30 second timeout
        
        try:
            command.upgrade(alembic_cfg, "head")
            signal.alarm(0)  # Cancel timeout
            print("✅ Database migration completed!")
            print("🎉 All advanced subscription fields should now be available in the database!")
        except TimeoutError:
            print("⏰ Migration timed out after 30 seconds")
            print("❌ Migration may have failed or is taking too long")
        except Exception as e:
            signal.alarm(0)  # Cancel timeout
            print(f"❌ Migration failed with error: {e}")
            raise
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
        # Run migration first (temporarily disabled)
        # run_migration()
        
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

# Debug endpoint to check database data
@app.get("/debug/data")
def debug_data():
    """Debug endpoint to check database data"""
    from .core.database import SessionLocal
    from .models.database import User, Subscription
    
    db = SessionLocal()
    try:
        # Count users
        user_count = db.query(User).count()
        
        # Count subscriptions
        subscription_count = db.query(Subscription).count()
        
        # Get first few users (without passwords)
        users = db.query(User).limit(5).all()
        user_list = []
        for user in users:
            user_list.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "is_premium": user.is_premium,
                "created_at": user.created_at
            })
        
        # Get first few subscriptions
        subscriptions = db.query(Subscription).limit(5).all()
        subscription_list = []
        for sub in subscriptions:
            subscription_list.append({
                "id": sub.id,
                "user_id": sub.user_id,
                "name": sub.name,
                "amount": sub.amount,
                "currency": sub.currency,
                "next_billing_date": sub.next_billing_date,
                "is_active": sub.is_active,
                "created_at": sub.created_at
            })
        
        return {
            "database_status": "connected",
            "user_count": user_count,
            "subscription_count": subscription_count,
            "users": user_list,
            "subscriptions": subscription_list
        }
    except Exception as e:
        return {
            "database_status": "error",
            "error": str(e)
        }
    finally:
        db.close()

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