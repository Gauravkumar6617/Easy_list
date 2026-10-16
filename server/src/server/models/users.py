from __future__ import annotations
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from server.db.database import Base
from typing import List as PyList, TYPE_CHECKING
from sqlalchemy.sql import func
if TYPE_CHECKING:
    from server.models.list import List


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(), 
        nullable=False
    )

    # 2. Automatically updates the timestamp whenever the user record changes
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )

    # Relationship to lists (plural, because one user can have MANY lists)
    lists: Mapped[PyList["List"]] = relationship("List", back_populates="user", cascade="all, delete-orphan")