from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import schemas
from .deps import get_db, get_current_user
from ..services import AlertService, NotificationService, UserPreferenceService
from ..models import User

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/alerts", response_model=List[schemas.Alert])
async def get_user_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    alert_service = AlertService(db)
    return alert_service.get_alerts_for_user(current_user.id)

@router.get("/notifications", response_model=List[schemas.Notification])
async def get_user_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notification_service = NotificationService(db)
    return notification_service.get_user_notifications(current_user.id)

@router.put("/alerts/{alert_id}/preferences", response_model=schemas.Preference)
async def update_alert_preferences(
    alert_id: int,
    preferences: schemas.PreferenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pref_service = UserPreferenceService(db)
    return pref_service.create_or_update_preference(
        user_id=current_user.id,
        alert_id=alert_id,
        is_read=preferences.is_read,
        snooze=preferences.snooze
    )

@router.post("/alerts/{alert_id}/read", response_model=schemas.Preference)
async def mark_alert_read(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pref_service = UserPreferenceService(db)
    return pref_service.mark_read(current_user.id, alert_id)

@router.post("/alerts/{alert_id}/unread", response_model=schemas.Preference)
async def mark_alert_unread(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pref_service = UserPreferenceService(db)
    return pref_service.mark_unread(current_user.id, alert_id)

@router.post("/alerts/{alert_id}/snooze", response_model=schemas.Preference)
async def snooze_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pref_service = UserPreferenceService(db)
    return pref_service.snooze_alert(current_user.id, alert_id)