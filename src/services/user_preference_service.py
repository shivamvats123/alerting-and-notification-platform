from datetime import datetime, timedelta
from ..models import UserAlertPreference
from .base import BaseService

class UserPreferenceService(BaseService):
    def __init__(self, db):
        super().__init__(db, UserAlertPreference)

    def get_user_preference(self, user_id, alert_id):
        return (
            self.db.query(UserAlertPreference)
            .filter_by(user_id=user_id, alert_id=alert_id)
            .first()
        )

    def create_or_update_preference(
        self, user_id, alert_id, is_read=None, snooze=None
    ):
        preference = self.get_user_preference(user_id, alert_id)
        
        if not preference:
            preference = UserAlertPreference(user_id=user_id, alert_id=alert_id)
            self.db.add(preference)
        
        if is_read is not None:
            preference.is_read = is_read
            
        if snooze:
            # Snooze until start of next day
            tomorrow = datetime.utcnow() + timedelta(days=1)
            preference.snoozed_until = datetime(
                tomorrow.year, tomorrow.month, tomorrow.day, 
                0, 0, 0  # Reset to start of day
            )
        
        self.db.commit()
        self.db.refresh(preference)
        return preference

    def mark_read(self, user_id, alert_id):
        return self.create_or_update_preference(user_id, alert_id, is_read=True)

    def mark_unread(self, user_id, alert_id):
        return self.create_or_update_preference(user_id, alert_id, is_read=False)

    def snooze_alert(self, user_id, alert_id):
        return self.create_or_update_preference(user_id, alert_id, snooze=True)