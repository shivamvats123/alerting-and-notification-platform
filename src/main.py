import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import admin_router, user_router, analytics_router
from .database import Base, engine
from .utils.scheduler import reminder_scheduler

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Alerting & Notification Platform",
    description="A lightweight alerting and notification system",
    version="1.0.0"
)

# Configure CORS with more specific settings
origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://alerting-and-notification-platform.onrender.com"
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

@app.on_event("startup")
async def startup_event():
    try:
        reminder_scheduler.start()
    except Exception as e:
        print(f"Error starting scheduler: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    try:
        reminder_scheduler.shutdown()
    except Exception as e:
        print(f"Error shutting down scheduler: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)