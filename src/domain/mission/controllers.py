from src.core.database import get_db

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import SessionLocal
from src.domain.mission.schemas import MissionCreate, MissionRead
from src.domain.mission.services import MissionService

router = APIRouter(prefix='/missions', tags=['Missions'])

def _svc(db: Session) -> MissionService:
  return MissionService(db)

_err = {
  'mission_not_found': (404, 'Mission not found'),
  'mission_assigned': (400, 'Mission already assigned to a cat'),
  'mission_already_assigned': (400, 'Mission already has a cat'),
  'cat_not_found': (404, 'Cat not found'),
  'cat_busy': (400, 'Cat busy with another mission'),
  'targets_incomplete': (400, 'All targets must be completed'),
}

def _raise(key: str):
  status_code, detail = _err.get(key, (400, key))
  raise HTTPException(status_code, detail)

# ─── endpoints ─────────────────────────────────────────────
@router.post(
  '',
  summary='Create mission (+ targets)',
  response_model=MissionRead,
  status_code=status.HTTP_201_CREATED,
)
def create(dto: MissionCreate, db: Session = Depends(get_db)):
  try:
    mission = _svc(db).create(dto)
    return MissionRead.model_validate(mission)
  except ValueError as e:
    _raise(e.args[0])

@router.get('', response_model=list[MissionRead])
def list_(db: Session = Depends(get_db)):
  missions = _svc(db).list()
  return [MissionRead.model_validate(m) for m in missions]

@router.get('/{mission_id}', response_model=MissionRead)
def get(mission_id: int, db: Session = Depends(get_db)):
  mission = _svc(db).get(mission_id)
  if not mission:
    raise HTTPException(404, 'Mission not found')
  return MissionRead.model_validate(mission)

@router.delete('/{mission_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(mission_id: int, db: Session = Depends(get_db)):
  try:
    _svc(db).delete(mission_id)
  except ValueError as e:
    _raise(e.args[0])

@router.patch('/{mission_id}/assign/{cat_id}', response_model=MissionRead)
def assign_cat(mission_id: int, cat_id: int, db: Session = Depends(get_db)):
  try:
    mission = _svc(db).assign_cat(mission_id, cat_id)
    return MissionRead.model_validate(mission)
  except ValueError as e:
    _raise(e.args[0])

@router.patch('/{mission_id}/complete', response_model=MissionRead)
def complete(mission_id: int, db: Session = Depends(get_db)):
  try:
    mission = _svc(db).complete(mission_id)
    return MissionRead.model_validate(mission)
  except ValueError as e:
    _raise(e.args[0])
