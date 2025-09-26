from datetime import datetime
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import Alert, Team, User, UserAlertPreference
from .base import BaseService

class AlertService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Alert)

    def create_alert(self, 
                    title: str,
                    message: str,
                    severity: str,
                    created_by_id: int,
                    org_wide: bool = False,
                    team_ids: List[int] = None,
                    user_ids: List[int] = None,
                    start_time: datetime = None,
                    expiry_time: datetime = None) -> Alert:
        
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

    def get_active_alerts(self) -> List[Alert]:
        now = datetime.utcnow()
        return (
            self.db.query(Alert)
            .filter(Alert.is_active == True)
            .filter(Alert.start_time <= now)
            .filter((Alert.expiry_time == None) | (Alert.expiry_time >= now))
            .all()
        )

    def get_alerts_for_user(self, user_id: int) -> List[Alert]:
        user = self.db.query(User).get(user_id)
        if not user:
            return []

        now = datetime.utcnow()
        alerts = (
            self.db.query(Alert)
            .filter(Alert.is_active == True)
            .filter(Alert.start_time <= now)
            .filter((Alert.expiry_time == None) | (Alert.expiry_time >= now))
            .filter(
                (Alert.org_wide == True) |
                (Alert.teams.any(id=user.team_id)) |
                (Alert.specific_users.any(id=user_id))
            )
            .all()
        )
        return alerts

    def archive_alert(self, alert_id: int) -> Optional[Alert]:
        return self.update(alert_id, is_active=False)