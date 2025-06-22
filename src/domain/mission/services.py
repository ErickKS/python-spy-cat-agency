from typing import List, Sequence
from sqlalchemy.orm import Session

from src.domain.mission.models import Mission
from src.domain.mission.repository import MissionRepository
from src.domain.mission.schemas import MissionCreate
from src.domain.target.models import Target
from src.domain.target.repository import TargetRepository
from src.domain.cat.models import Cat

class MissionService:
  def __init__(self, db: Session) -> None:
    self.db = db
    self.missions = MissionRepository(db)
    self.targets = TargetRepository(db)

  def create(self, dto: MissionCreate) -> Mission:
    if dto.cat_id:
      self._assert_cat_available(dto.cat_id)

    mission = Mission(cat_id=dto.cat_id)
    mission.targets = [Target(**t.model_dump()) for t in dto.targets]

    self.missions.create(mission)
    self.missions.commit()
    self.missions.refresh(mission)
    return mission

  def list(self) -> Sequence[Mission]:
    return self.missions.find_many()

  def get(self, mission_id: int) -> Mission | None:
    return self.missions.get_by_id(mission_id)

  def delete(self, mission_id: int) -> None:
    mission = self.missions.get_by_id(mission_id)
    if not mission:
      raise ValueError('mission_not_found')
    if mission.cat_id:
      raise ValueError('mission_assigned')
    self.db.delete(mission)
    self.missions.commit()

  def assign_cat(self, mission_id: int, cat_id: int) -> Mission:
    mission = self.missions.get_by_id(mission_id)
    if not mission:
      raise ValueError('mission_not_found')
    self._assert_cat_available(cat_id)

    if mission.cat_id:
      raise ValueError('mission_already_assigned')

    mission.cat_id = cat_id
    self.missions.commit()
    self.missions.refresh(mission)
    return mission

  def complete(self, mission_id: int) -> Mission:
    mission = self.missions.get_by_id(mission_id)
    if not mission:
      raise ValueError('mission_not_found')
    if any(not t.completed for t in mission.targets):
      raise ValueError('targets_incomplete')
    mission.completed = True
    self.missions.commit()
    self.missions.refresh(mission)
    return mission

  def _assert_cat_available(self, cat_id: int) -> None:
    cat = self.db.query(Cat).get(cat_id)
    if not cat:
      raise ValueError('cat_not_found')
    if any(not m.completed for m in cat.missions):
      raise ValueError('cat_busy')
