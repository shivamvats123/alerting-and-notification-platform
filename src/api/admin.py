from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import schemas
from .deps import get_db, get_current_admin
from ..services import AlertService
from ..models import User

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/alerts", response_model=schemas.Alert)
async def create_alert(
    alert: schemas.AlertCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    alert_service = AlertService(db)
    return alert_service.create_alert(
        title=alert.title,
        message=alert.message,
        severity=alert.severity,
        created_by_id=current_admin.id,
        org_wide=alert.org_wide,
        team_ids=alert.team_ids,
        user_ids=alert.user_ids,
        start_time=alert.start_time,
        expiry_time=alert.expiry_time
    )

@router.get("/alerts", response_model=List[schemas.Alert])
async def list_alerts(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    alert_service = AlertService(db)
    return alert_service.get_all()

@router.put("/alerts/{alert_id}/archive", response_model=schemas.Alert)
async def archive_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    alert_service = AlertService(db)
    alert = alert_service.archive_alert(alert_id)
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    return alert