from datetime import datetime
from typing import Optional

from sqlalchemy import Enum, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.utils.enums import defaultStatusEnum


class User(Base):
    __tablename__="user"

    id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,index=True,unique=True);
    email:Mapped[str] = mapped_column(String(120), index=True, unique=True);
    password:Mapped[str] = mapped_column(String(60));
    username:Mapped[Optional[str]] = mapped_column(String(60), nullable=True, default=None)

    ## Relationships
    appointments = relationship("appointment", back_populates="user")

    ## Colunas com valores padrões
    created_at:Mapped[Optional[datetime]] = mapped_column(DateTime,nullable=True,default=None)
    updated_at:Mapped[Optional[datetime]] = mapped_column(DateTime,nullable=True,default=None)
    deleted_at:Mapped[Optional[datetime]] = mapped_column(DateTime,nullable=True,default=None)
    
    status:Mapped[defaultStatusEnum] = mapped_column(Enum(defaultStatusEnum), default=defaultStatusEnum.ACTIVE)

    def __init__(
            self, 
            id=None,
            email=None,
            password=None,
            username=None,
            created_at=None,
            updated_at=None,
            deleted_at=None
        ):
        self.username = username; 
        self.password = password;
        self.created_at = created_at;
        self.email = email;
        self.deleted_at = deleted_at;
        self.updated_at = updated_at;
        self.id = id;