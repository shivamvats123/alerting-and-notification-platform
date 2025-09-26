from datetime import datetime, timedelta
from ..src.services import AlertService
from ..src.models.enums import AlertSeverity

def test_create_alert(db_session, test_admin, test_team):
    service = AlertService(db_session)
    alert = service.create_alert(
        title="Test Alert",
        message="This is a test alert",
        severity=AlertSeverity.INFO,
        created_by_id=test_admin.id,
        org_wide=False,
        team_ids=[test_team.id]
    )
    
    assert alert.title == "Test Alert"
    assert alert.message == "This is a test alert"
    assert alert.severity == AlertSeverity.INFO
    assert alert.created_by_id == test_admin.id
    assert len(alert.teams) == 1
    assert alert.teams[0].id == test_team.id

def test_get_active_alerts(db_session, test_admin):
    service = AlertService(db_session)
    
    # Create an active alert
    active_alert = service.create_alert(
        title="Active Alert",
        message="This is active",
        severity=AlertSeverity.INFO,
        created_by_id=test_admin.id,
        org_wide=True
    )
    
    # Create an expired alert
    expired_alert = service.create_alert(
        title="Expired Alert",
        message="This is expired",
        severity=AlertSeverity.INFO,
        created_by_id=test_admin.id,
        org_wide=True,
        expiry_time=datetime.utcnow() - timedelta(days=1)
    )
    
    active_alerts = service.get_active_alerts()
    assert len(active_alerts) == 1
    assert active_alerts[0].id == active_alert.id

def test_get_alerts_for_user(db_session, test_admin, test_user, test_team):
    service = AlertService(db_session)
    
    # Update test user with team
    test_user.team_id = test_team.id
    db_session.commit()
    
    # Create different types of alerts
    org_alert = service.create_alert(
        title="Org Alert",
        message="For everyone",
        severity=AlertSeverity.INFO,
        created_by_id=test_admin.id,
        org_wide=True
    )
    
    team_alert = service.create_alert(
        title="Team Alert",
        message="For the team",
        severity=AlertSeverity.WARNING,
        created_by_id=test_admin.id,
        team_ids=[test_team.id]
    )
    
    user_alert = service.create_alert(
        title="User Alert",
        message="Just for you",
        severity=AlertSeverity.CRITICAL,
        created_by_id=test_admin.id,
        user_ids=[test_user.id]
    )
    
    user_alerts = service.get_alerts_for_user(test_user.id)
    assert len(user_alerts) == 3  # Should see org, team, and personal alerts