from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..models import Alert, NotificationDelivery, UserAlertPreference
from ..models.enums import AlertSeverity

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_alert_metrics(self, days: int = 30):
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        # Total alerts created
        total_alerts = (
            self.db.query(Alert)
            .filter(Alert.created_at >= start_date)
            .count()
        )

        # Alerts by severity
        alerts_by_severity = (
            self.db.query(
                Alert.severity,
                func.count(Alert.id).label('count')
            )
            .filter(Alert.created_at >= start_date)
            .group_by(Alert.severity)
            .all()
        )
        severity_counts = {
            severity.value: 0 for severity in AlertSeverity
        }
        for severity, count in alerts_by_severity:
            severity_counts[severity.value] = count

        # Alerts delivered vs read
        delivered_count = (
            self.db.query(func.count(NotificationDelivery.id))
            .filter(NotificationDelivery.delivered_at >= start_date)
            .scalar()
        )

        read_count = (
            self.db.query(func.count(UserAlertPreference.id))
            .filter(UserAlertPreference.is_read == True)
            .join(Alert)
            .filter(Alert.created_at >= start_date)
            .scalar()
        )

        # Snoozed alerts
        snoozed_count = (
            self.db.query(func.count(UserAlertPreference.id))
            .filter(UserAlertPreference.snoozed_until.isnot(None))
            .join(Alert)
            .filter(Alert.created_at >= start_date)
            .scalar()
        )

        return {
            "period_days": days,
            "total_alerts": total_alerts,
            "alerts_by_severity": severity_counts,
            "total_delivered": delivered_count,
            "total_read": read_count,
            "total_snoozed": snoozed_count,
            "read_rate": round(read_count / delivered_count * 100, 2) if delivered_count > 0 else 0
        }