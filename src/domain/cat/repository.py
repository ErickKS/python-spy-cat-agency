from typing import List, Sequence
from sqlalchemy.orm import Session
from src.domain.cat.models import Cat

class CatRepository:
  def __init__(self, db: Session) -> None:
      self._db = db

  def find_many(self) -> List[Cat]:
    return self._db.query(Cat).order_by(Cat.id).all()

  def get_by_id(self, cat_id: int) -> Cat | None:
    return self._db.query(Cat).filter(Cat.id == cat_id).first()

  def create(self, cat: Cat) -> None:
    self._db.add(cat)

  def delete(self, cat: Cat) -> None:
    self._db.delete(cat)

  def commit(self) -> None:
    self._db.commit()

  def refresh(self, cat: Cat, attrs: Sequence[str] | None = None) -> None:
    self._db.refresh(cat, attribute_names=attrs)
