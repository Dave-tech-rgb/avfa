from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from database import Base

class Device(Base):
    __tablename__ = "api_device"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    location = Column(String(100))
    status = Column(String(20), default="Online")
    device_id = Column(String(255))
    created_at = Column(DateTime, default=func.now())

class SystemUser(Base):
    __tablename__ = "api_systemuser"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    role = Column(String(20), default="Viewer")
    created_at = Column(DateTime, default=func.now())

class AuditLog(Base):
    __tablename__ = "api_auditlog"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(100))
    user = Column(String(100))
    role = Column(String(50))
    timestamp = Column(DateTime, default=func.now())

class AuthUser(Base):
    __tablename__ = "auth_user"
    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(128))
    last_login = Column(DateTime, nullable=True)
    is_superuser = Column(Integer, default=0)
    username = Column(String(150), unique=True)
    first_name = Column(String(150), default="")
    last_name = Column(String(150), default="")
    email = Column(String(254), default="")
    is_staff = Column(Integer, default=0)
    is_active = Column(Integer, default=1)
    date_joined = Column(DateTime, default=func.now())

from sqlalchemy import Float

class DetectionSession(Base):
    __tablename__ = "api_detectionsession"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"), nullable=True)
    car_count = Column(Integer, default=0)
    truck_count = Column(Integer, default=0)
    bus_count = Column(Integer, default=0)
    motorcycle_count = Column(Integer, default=0)
    average_confidence = Column(Float, default=0.0)
    video_url = Column(String(255), nullable=True)
    timestamp = Column(DateTime, default=func.now())
