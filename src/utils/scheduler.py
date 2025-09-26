from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..services import NotificationService

class ReminderScheduler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ReminderScheduler, cls).__new__(cls)
            cls._instance.scheduler = BackgroundScheduler()
            cls._instance.setup_jobs()
        return cls._instance

    def setup_jobs(self):
        # Add job to process reminders every minute
        self.scheduler.add_job(
            self.process_reminders,
            trigger=IntervalTrigger(minutes=1),
            id='process_reminders',
            replace_existing=True
        )

    def start(self):
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()

    def process_reminders(self):
        # Create a new database session for this background job
        db = SessionLocal()
        try:
            notification_service = NotificationService(db)
            notification_service.process_reminders()
        finally:
            db.close()

# Create a singleton instance
reminder_scheduler = ReminderScheduler()