from datetime import datetime, timedelta
from ..src.services import NotificationService, AlertService, UserPreferenceService
from ..src.models.enums import AlertSeverity

def test_create_notification(db_session, test_user):
    alert_service = AlertService(db_session)
    notification_service = NotificationService(db_session)
    
    # Create an alert
    alert = alert_service.create_alert(
        title="Test Alert",
        message="Test message",
        severity=AlertSeverity.INFO,
        created_by_id=test_user.id,
        org_wide=True
    )
    
    # Create a notification
    notification = notification_service.create_notification(
        user_id=test_user.id,
        alert_id=alert.id
    )
    
    assert notification.user_id == test_user.id
    assert notification.alert_id == alert.id
    assert notification.status == "success"
    assert notification.delivery_type == "in_app"

def test_get_pending_reminders(db_session, test_user):
    alert_service = AlertService(db_session)
    notification_service = NotificationService(db_session)
    pref_service = UserPreferenceService(db_session)
    
    # Create an alert
    alert = alert_service.create_alert(
        title="Test Alert",
        message="Test message",
        severity=AlertSeverity.INFO,
        created_by_id=test_user.id,
        org_wide=True
    )
    
    # Create initial preference
    pref_service.create_or_update_preference(
        user_id=test_user.id,
        alert_id=alert.id
    )
    
    # Should be pending since it's never been sent
    pending = notification_service.get_pending_reminders()
    assert len(pending) == 1
    assert pending[0][0].id == test_user.id
    assert pending[0][1].id == alert.id
    
    # Create notification and update last reminded time
    notification_service.process_reminders()
    
    # Should not be pending anymore (within 2 hour window)
    pending = notification_service.get_pending_reminders()
    assert len(pending) == 0

def test_get_user_notifications(db_session, test_user):
    alert_service = AlertService(db_session)
    notification_service = NotificationService(db_session)
    
    # Create multiple alerts and notifications
    alert1 = alert_service.create_alert(
        title="Alert 1",
        message="First alert",
        severity=AlertSeverity.INFO,
        created_by_id=test_user.id,
        org_wide=True
    )
    
    alert2 = alert_service.create_alert(
        title="Alert 2",
        message="Second alert",
        severity=AlertSeverity.WARNING,
        created_by_id=test_user.id,
        org_wide=True
    )
    
    notification_service.create_notification(test_user.id, alert1.id)
    notification_service.create_notification(test_user.id, alert2.id)
    
    notifications = notification_service.get_user_notifications(test_user.id)
    assert len(notifications) == 2