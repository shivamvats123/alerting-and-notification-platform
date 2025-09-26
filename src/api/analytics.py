from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Union
from .deps import get_db, get_current_admin
from ..services.analytics_service import AnalyticsService
from ..models import User

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/metrics")
async def get_metrics(
    days: int = 30,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
) -> Dict[str, Union[int, float, dict]]:
    analytics_service = AnalyticsService(db)
    return analytics_service.get_alert_metrics(days)