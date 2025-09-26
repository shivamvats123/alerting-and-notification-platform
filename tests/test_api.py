from datetime import datetime
import pytest
from ..src.api import deps
from ..src.models.enums import AlertSeverity

def override_get_current_admin(test_admin):
    async def _get_current_admin():
        return test_admin
    return _get_current_admin

def override_get_current_user(test_user):
    async def _get_current_user():
        return test_user
    return _get_current_user

def test_create_alert(client, test_admin, monkeypatch):
    monkeypatch.setattr(deps, "get_current_admin", override_get_current_admin(test_admin))
    
    response = client.post(
        "/admin/alerts",
        json={
            "title": "Test Alert",
            "message": "This is a test alert",
            "severity": "info",
            "org_wide": True
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Alert"
    assert data["severity"] == "info"
    assert data["org_wide"] == True

def test_list_alerts(client, test_admin, monkeypatch):
    monkeypatch.setattr(deps, "get_current_admin", override_get_current_admin(test_admin))
    
    # Create a test alert first
    client.post(
        "/admin/alerts",
        json={
            "title": "Test Alert",
            "message": "This is a test alert",
            "severity": "info",
            "org_wide": True
        }
    )
    
    response = client.get("/admin/alerts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Alert"

def test_get_user_alerts(client, test_user, test_admin, monkeypatch):
    monkeypatch.setattr(deps, "get_current_admin", override_get_current_admin(test_admin))
    monkeypatch.setattr(deps, "get_current_user", override_get_current_user(test_user))
    
    # Create a test alert first
    client.post(
        "/admin/alerts",
        json={
            "title": "Test Alert",
            "message": "This is a test alert",
            "severity": "info",
            "org_wide": True
        }
    )
    
    response = client.get("/user/alerts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Alert"

def test_snooze_alert(client, test_user, test_admin, monkeypatch):
    monkeypatch.setattr(deps, "get_current_admin", override_get_current_admin(test_admin))
    monkeypatch.setattr(deps, "get_current_user", override_get_current_user(test_user))
    
    # Create a test alert first
    alert_response = client.post(
        "/admin/alerts",
        json={
            "title": "Test Alert",
            "message": "This is a test alert",
            "severity": "info",
            "org_wide": True
        }
    )
    alert_id = alert_response.json()["id"]
    
    # Snooze the alert
    response = client.post(f"/user/alerts/{alert_id}/snooze")
    assert response.status_code == 200
    data = response.json()
    assert data["alert_id"] == alert_id
    assert data["snoozed_until"] is not None