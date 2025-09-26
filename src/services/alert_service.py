from datetime import datetime
from ..models import Alert, Team, User, UserAlertPreference
from .base import BaseService

class AlertService(BaseService):
    def __init__(self, db):
        super().__init__(db, Alert)

    def create_alert(self, 
                    title,
                    message,
                    severity,
                    created_by_id,
                    org_wide=False,
                    team_ids=None,
                    user_ids=None,
                    start_time=None,
                    expiry_time=None):
        
        alert = Alert(
            title=title,
            message=message,
            severity=severity,
            created_by_id=created_by_id,
            org_wide=org_wide,
            start_time=start_time or datetime.utcnow(),
            expiry_time=expiry_time,
            delivery_type="in_app"  # Default for MVP
        )
        
        if team_ids:
            teams = self.db.query(Team).filter(Team.id.in_(team_ids)).all()
            alert.teams = teams
            
        if user_ids:
            users = self.db.query(User).filter(User.id.in_(user_ids)).all()
            alert.specific_users = users
            
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def get_active_alerts(self):
        now = datetime.utcnow()
        return (
            self.db.query(Alert)
            .filter(Alert.is_active == True)
            .filter(Alert.start_time <= now)
            .filter((Alert.expiry_time == None) | (Alert.expiry_time >= now))
            .all()
        )

    def get_alerts_for_user(self, user_id):
        """Get all alerts that are visible to a user."""
        now = datetime.utcnow()
        return (
            self.db.query(Alert)
            .filter(Alert.is_active == True)
            .filter(Alert.start_time <= now)
            .filter((Alert.expiry_time == None) | (Alert.expiry_time >= now))
            .filter(
                (Alert.org_wide == True) |
                (Alert.specific_users.any(id=user_id)) |
                (Alert.teams.any(Team.members.any(id=user_id)))
            )
            .all()
        )

    def archive_alert(self, alert_id):
        alert = self.get(alert_id)
        if alert:
            alert.is_active = False
            self.db.commit()
            self.db.refresh(alert)
            return alert
        return None