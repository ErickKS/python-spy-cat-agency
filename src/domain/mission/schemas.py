from datetime import datetime
from typing import List, Optional, Annotated

from pydantic import BaseModel, ConfigDict, conlist

from src.domain.target.schemas import TargetCreate, TargetRead

class MissionCreate(BaseModel):
  cat_id: Optional[int] = None
  targets: Annotated[List[TargetCreate], conlist(TargetCreate, min_length=1, max_length=3)]

class MissionRead(BaseModel):
  id: int
  completed: bool
  cat_id: Optional[int]
  targets: List[TargetRead]

  model_config = ConfigDict(from_attributes=True)