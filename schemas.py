from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DeviceBase(BaseModel):
    name: str
    location: str
    status: Optional[str] = "Online"
    deviceId: str = Field(alias="deviceId", validation_alias="deviceId", serialization_alias="deviceId", default="")

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    model_config = {"from_attributes": True, "populate_by_name": True}

class SystemUserBase(BaseModel):
    name: str
    role: str

class SystemUserCreate(SystemUserBase):
    pass

class SystemUser(SystemUserBase):
    id: int
    model_config = {"from_attributes": True}

class AuditLogBase(BaseModel):
    action: str
    user: str
    role: str

class AuditLogCreate(AuditLogBase):
    pass

class AuditLog(AuditLogBase):
    id: int
    time: str

    model_config = {"from_attributes": True}

class UserLogin(BaseModel):
    email: str
    password: str

class DetectionSessionCreate(BaseModel):
    user_id: Optional[int] = None
    car_count: int = 0
    truck_count: int = 0
    bus_count: int = 0
    motorcycle_count: int = 0
    average_confidence: float = 0.0

class DetectionSessionResponse(DetectionSessionCreate):
    id: int
    video_url: Optional[str] = None
    timestamp: datetime
    model_config = {"from_attributes": True}
