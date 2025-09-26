import os
from datetime import timedelta

# JWT Settings
SECRET_KEY = os.environ.get("SECRET_KEY", "your-super-secret-key-for-development")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Email Settings (for future use)
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")

# Application Settings
APP_NAME = os.environ.get("APP_NAME", "Alerting & Notification Platform")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
DEBUG = ENVIRONMENT == "development"

# Reminder Settings
DEFAULT_REMINDER_INTERVAL = int(os.environ.get("DEFAULT_REMINDER_INTERVAL", "7200"))  # 2 hours in seconds