from datetime import datetime, timedelta
from ..models import NotificationDelivery, UserAlertPreference, Alert, User
from .base import BaseService

class NotificationService(BaseService):
    def __init__(self, db):
        super().__init__(db, NotificationDelivery)
        self.REMINDER_INTERVAL = timedelta(hours=2)

    def create_notification(self, user_id, alert_id):
        notification = NotificationDelivery(
            user_id=user_id,
            alert_id=alert_id,
            delivery_type="in_app",
            status="success"
        )
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def get_pending_reminders(self):
        now = datetime.utcnow()
        preferences = (
            self.db.query(UserAlertPreference)
            .join(Alert)
            .join(User)
            .filter(
                Alert.is_active == True,
                Alert.start_time <= now,
                (Alert.expiry_time == None) | (Alert.expiry_time >= now),
                (UserAlertPreference.snoozed_until == None) | 
                (UserAlertPreference.snoozed_until <= now),
                (UserAlertPreference.last_reminded_at == None) |
                (UserAlertPreference.last_reminded_at <= now - self.REMINDER_INTERVAL)
            )
            .all()
        )
        
        return [(pref.user, pref.alert) for pref in preferences]

    def process_reminders(self):
        for user, alert in self.get_pending_reminders():
            # Create new notification
            self.create_notification(user.id, alert.id)
            
            # Update last reminded time
            preference = (
                self.db.query(UserAlertPreference)
                .filter_by(user_id=user.id, alert_id=alert.id)
                .first()
            )
            if preference:
                preference.last_reminded_at = datetime.utcnow()
                self.db.commit()