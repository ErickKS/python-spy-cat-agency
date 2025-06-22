from datetime import datetime, timezone
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base

if TYPE_CHECKING:
  from src.domain.cat.models import Cat
  from src.domain.target.models import Target

class Mission(Base):
  __tablename__ = 'missions'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  cat_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('cats.id'))
  completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
  created_at: Mapped[datetime] = mapped_column(
    DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
  )
  updated_at: Mapped[datetime] = mapped_column(
    DateTime,
    default=lambda: datetime.now(timezone.utc),
    onupdate=lambda: datetime.now(timezone.utc),
  )

  cat: Mapped[Optional['Cat']] = relationship(back_populates='missions')
  targets: Mapped[List['Target']] = relationship(
    cascade='all, delete-orphan', back_populates='mission'
  )