import os
import logging
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .api import admin_router, user_router, analytics_router
from .database import Base, engine
from .utils.scheduler import reminder_scheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title="Alerting & Notification Platform",
    description="A lightweight alerting and notification system",
    version="1.0.0",
    docs_url="/docs" if os.getenv("ENVIRONMENT") != "production" else None,
    redoc_url="/redoc" if os.getenv("ENVIRONMENT") != "production" else None,
)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://alerting-and-notification-platform.onrender.com",
    "https://*.render.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if os.getenv("ENVIRONMENT") == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(analytics_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Alerting & Notification Platform API",
        "docs_url": "/docs",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error occurred: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error occurred"}
    )

@app.on_event("startup")
async def startup_event():
    try:
        # Create database tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # Start the reminder scheduler
        reminder_scheduler.start()
        logger.info("Reminder scheduler started successfully")
    except Exception as e:
        logger.error(f"Error during startup: {e}", exc_info=True)
        raise

@app.on_event("shutdown")
async def shutdown_event():
    try:
        reminder_scheduler.shutdown()
    except Exception as e:
        print(f"Error shutting down scheduler: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)