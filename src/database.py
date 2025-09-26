import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get environment variables with defaults
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./notification_platform.db")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")

# Configure database URL based on environment
if ENVIRONMENT == "production":
    # Convert postgres:// to postgresql:// for SQLAlchemy
    SQLALCHEMY_DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")
else:
    SQLALCHEMY_DATABASE_URL = DATABASE_URL

# Configure SQLAlchemy engine
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()