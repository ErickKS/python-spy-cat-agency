from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from src.core.cat_api import assert_valid_breed

class CatBase(BaseModel):
  name: str = Field(max_length=60)
  years_experience: int = Field(ge=0)
  breed: str = Field(max_length=60)
  salary: float = Field(gt=0)

class CatCreate(CatBase):
  pass

class CatUpdate(BaseModel):
  salary: float = Field(..., gt=0)

class CatRead(CatBase):
  id: int
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)