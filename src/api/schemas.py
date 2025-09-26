from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from ..models.enums import AlertSeverity, DeliveryType

# User schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    team_id: Optional[int] = None
    is_admin: bool = False

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True

# Team schemas
class TeamBase(BaseModel):
    name: str

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    
    class Config:
        orm_mode = True

# Alert schemas
class AlertBase(BaseModel):
    title: str
    message: str
    severity: AlertSeverity
    org_wide: bool = False
    team_ids: Optional[List[int]] = None
    user_ids: Optional[List[int]] = None
    start_time: Optional[datetime] = None
    expiry_time: Optional[datetime] = None

class AlertCreate(AlertBase):
    pass

class Alert(AlertBase):
    id: int
    created_at: datetime
    is_active: bool
    created_by_id: int
    
    class Config:
        orm_mode = True

# Preference schemas
class PreferenceUpdate(BaseModel):
    is_read: Optional[bool] = None
    snooze: Optional[bool] = None

class Preference(BaseModel):
    id: int
    user_id: int
    alert_id: int
    is_read: bool
    snoozed_until: Optional[datetime]
    last_reminded_at: Optional[datetime]
    
    class Config:
        orm_mode = True

# Notification schemas
class Notification(BaseModel):
    id: int
    user_id: int
    alert_id: int
    delivered_at: datetime
    delivery_type: DeliveryType
    status: str
    
    class Config:
        orm_mode = True