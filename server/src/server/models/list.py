from __future__ import annotations
from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from server.db.database import Base
from typing import TYPE_CHECKING
from sqlalchemy.sql import func
if TYPE_CHECKING:
    from server.models.users import User


class List(Base):
    __tablename__ = "lists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
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

    
    # Foreign key pointing to the user who created it (with an index for fast lookups)
    created_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    
    # Relationship back to the User model (singular because a list belongs to ONE user)
    user: Mapped["User"] = relationship("User", back_populates="lists")