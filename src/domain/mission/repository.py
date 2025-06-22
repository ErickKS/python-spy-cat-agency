from typing import List, Sequence
from sqlalchemy.orm import Session

from src.domain.mission.models import Mission

class MissionRepository:
    def __init__(self, db: Session) -> None:
      self._db = db

    def find_many(self) -> List[Mission]:
      return self._db.query(Mission).order_by(Mission.id).all()

    def get_by_id(self, mission_id: int) -> Mission | None:
      return self._db.query(Mission).filter(Mission.id == mission_id).first()

    def create(self, mission: Mission) -> None:
      self._db.add(mission)

    def refresh(self, obj) -> None:
      self._db.refresh(obj)

    def commit(self) -> None:
        self._db.commit()
