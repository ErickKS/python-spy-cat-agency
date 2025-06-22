from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.domain.cat.models import Cat
from src.domain.cat.repository import CatRepository
from src.domain.cat.schemas import CatCreate, CatUpdate
from src.core.cat_api import assert_valid_breed

class CatService:
  def __init__(self, db: Session) -> None:
      self._repo = CatRepository(db)

  def find_many(self) -> List[Cat]:
      return self._repo.find_many()

  def get_by_id(self, cat_id: int) -> Cat:
    cat = self._repo.get_by_id(cat_id)
    if not cat:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Cat not found'
      )
    return cat

  def create(self, dto: CatCreate) -> Cat:
    try:
      assert_valid_breed(dto.breed)
    except ValueError as e:
      raise ValueError(str(e))
    cat = Cat(**dto.model_dump())
    self._repo.create(cat)
    self._repo.commit()
    self._repo.refresh(cat)
    return cat

  def update(self, cat_id: int, dto: CatUpdate) -> Cat:
    cat = self.get_by_id(cat_id)
    for key, value in dto.model_dump(exclude_none=True).items():
      setattr(cat, key, value)
    self._repo.commit()
    self._repo.refresh(cat)
    return cat

  def delete(self, cat_id: int) -> None:
    cat = self.get_by_id(cat_id)
    self._repo.delete(cat)
    self._repo.commit()
