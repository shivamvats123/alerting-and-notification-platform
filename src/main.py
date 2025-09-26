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

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    return {"message": "Welcome to the Alerting & Notification Platform API"}

@app.on_event("startup")
async def startup_event():
    reminder_scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    reminder_scheduler.shutdown()