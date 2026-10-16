from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from server.db.database import Base
from server.models.list import List
from server.models.users import User

class SharedList(Base):
    __tablename__ = "shared_lists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # 1. Fixed typo to 'ForeignKey' and added 'index=True' for performance
    list_id: Mapped[int] = mapped_column(ForeignKey("lists.id"), index=True, nullable=False)
    shared_with_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    
    # Optional metadata for sharing
    can_edit: Mapped[bool] = mapped_column(Boolean, default=False) # e.g., view-only vs collaborative
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 2. Add relationships so you can easily navigate from SharedList to User/List in Python
    list: Mapped["List"] = relationship("List")
    shared_with_user: Mapped["User"] = relationship("User")