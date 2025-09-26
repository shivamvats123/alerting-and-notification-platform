from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean, Table
from sqlalchemy.orm import relationship
from ..database import Base
from .enums import AlertSeverity, DeliveryType

# Association table for Alert-Team visibility
alert_team_association = Table(
    'alert_team_association',
    Base.metadata,
    Column('alert_id', Integer, ForeignKey('alerts.id')),
    Column('team_id', Integer, ForeignKey('teams.id'))
)

# Association table for Alert-User visibility
alert_user_association = Table(
    'alert_user_association',
    Base.metadata,
    Column('alert_id', Integer, ForeignKey('alerts.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    is_admin = Column(Boolean, default=False)
    team_id = Column(Integer, ForeignKey("teams.id"))
    
    team = relationship("Team", back_populates="users")
    preferences = relationship("UserAlertPreference", back_populates="user")
    notifications = relationship("NotificationDelivery", back_populates="user")

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    users = relationship("User", back_populates="team")
    alerts = relationship("Alert", secondary=alert_team_association, back_populates="teams")

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    message = Column(String)
    severity = Column(Enum(AlertSeverity))
    delivery_type = Column(Enum(DeliveryType))
    reminder_frequency = Column(Integer, default=7200)  # 2 hours in seconds
    org_wide = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    start_time = Column(DateTime)
    expiry_time = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))

    teams = relationship("Team", secondary=alert_team_association, back_populates="alerts")
    specific_users = relationship("User", secondary=alert_user_association)
    preferences = relationship("UserAlertPreference", back_populates="alert")
    deliveries = relationship("NotificationDelivery", back_populates="alert")

class UserAlertPreference(Base):
    __tablename__ = "user_alert_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    alert_id = Column(Integer, ForeignKey("alerts.id"))
    is_read = Column(Boolean, default=False)
    snoozed_until = Column(DateTime, nullable=True)
    last_reminded_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="preferences")
    alert = relationship("Alert", back_populates="preferences")

class NotificationDelivery(Base):
    __tablename__ = "notification_deliveries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    alert_id = Column(Integer, ForeignKey("alerts.id"))
    delivered_at = Column(DateTime, default=datetime.utcnow)
    delivery_type = Column(Enum(DeliveryType))
    status = Column(String)  # success, failed, pending

    user = relationship("User", back_populates="notifications")
    alert = relationship("Alert", back_populates="deliveries")