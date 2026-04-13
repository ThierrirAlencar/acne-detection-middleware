

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

# Consultas são as salas de conversa
class Appointment(Base):
    __tablename__="appointment" # Consultas

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True, unique=True);

    # Relationships
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="appointments")

    inquiries = relationship("Inquiry", back_populates="appointment")

    ## Colunas com valores padrões
    created_at:Mapped[Optional[datetime]] = mapped_column(DateTime,nullable=True,default=None)
    updated_at:Mapped[Optional[datetime]] = mapped_column(DateTime,nullable=True,default=None)
    deleted_at:Mapped[Optional[datetime]] = mapped_column(DateTime,nullable=True,default=None)
    
    def __init__(
            self, 
            id=None,
            created_at=None,
            updated_at=None,
            deleted_at=None,
            user_id=None
        ):
        self.created_at = created_at;
        self.deleted_at = deleted_at;
        self.updated_at = updated_at;
        self.id = id;
        self.user_id = user_id