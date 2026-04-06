from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.utils.enums import inquiryStatus

class Inquiry(Base):
    __tablename__ = "inquiry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True, unique=True);
    image_url:Mapped[str] = mapped_column(String(258), nullable=True);
    
    ## Results
    result_text:Mapped[str] = mapped_column(String(1280), nullable=True);
    result_json_url:Mapped[str] = mapped_column(String, nullable=True);
    result_image_url:Mapped[str] = mapped_column(String, nullable=True);

    # Relationships
    appointment_id:Mapped[int] = mapped_column(Integer, ForeignKey("appointment.id"))
    appointment = relationship("Appointment", back_populates="appointments")

    ## Colunas com valores padrões
    created_at:Mapped[Optional[datetime]] = mapped_column(DateTime,nullable=True,default=None)
    updated_at:Mapped[Optional[datetime]] = mapped_column(DateTime,nullable=True,default=None)
    deleted_at:Mapped[Optional[datetime]] = mapped_column(DateTime,nullable=True,default=None)
    
    inquiry_status:Mapped[inquiryStatus] = mapped_column(Enum(inquiryStatus), default=inquiryStatus.ONGOING)

    def __init__(
            self, 
            id=None,
            created_at=None,
            updated_at=None,
            deleted_at=None,
            appointment_id=None,
            inquiry_status=None,
            result_text=None,
            result_json_url=None,
            result_image_url=None
        ):
        self.created_at = created_at;
        self.deleted_at = deleted_at;
        self.updated_at = updated_at;
        self.id = id;
        self.result_image_url = result_image_url;
        self.result_json_url = result_json_url;
        self.result_text = result_text;
        self.appointment_id = appointment_id;
        self.inquiry_status = inquiry_status;