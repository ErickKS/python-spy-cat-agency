from datetime import datetime, timezone
from typing import List, TYPE_CHECKING
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base

if TYPE_CHECKING:
  from src.domain.mission.models import Mission

class Cat(Base):
  __tablename__ = 'cats'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(60), nullable=False)
  years_experience: Mapped[int] = mapped_column(Integer, nullable=False)
  breed: Mapped[str] = mapped_column(String(60), nullable=False)
  salary: Mapped[float] = mapped_column(Float, nullable=False)
  created_at: Mapped[datetime] = mapped_column(
    DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
  )
  updated_at: Mapped[datetime] = mapped_column(
    DateTime,
    default=lambda: datetime.now(timezone.utc),
    onupdate=lambda: datetime.now(timezone.utc),
  )
  missions: Mapped[List['Mission']] = relationship(back_populates='cat')