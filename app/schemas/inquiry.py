from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.utils.enums import inquiryStatus

class InquiryBase(BaseModel):
    appointment_id: int
    image_url: Optional[str] = None

class InquiryCreate(InquiryBase):
    inquiry_status: Optional[inquiryStatus] = inquiryStatus.ONGOING

class InquiryUpdate(BaseModel):
    image_url: Optional[str] = None
    result_text: Optional[str] = None
    result_json_url: Optional[str] = None
    result_image_url: Optional[str] = None
    inquiry_status: Optional[inquiryStatus] = None

class InquiryParams(BaseModel):
    id: int

class InquiryResponse(InquiryBase):
    id: int
    result_text: Optional[str] = None
    result_json_url: Optional[str] = None
    result_image_url: Optional[str] = None
    inquiry_status: inquiryStatus
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True

class InquiryPublic(InquiryResponse):
    pass
