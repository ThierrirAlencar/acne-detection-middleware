from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class AppointmentBase(BaseModel):
    user_id: int

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    user_id: Optional[int] = None

class AppointmentParams(BaseModel):
    id: int

class AppointmentResponse(AppointmentBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True

class AppointmentPublic(AppointmentResponse):
    pass
