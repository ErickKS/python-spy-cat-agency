from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.domain.cat.schemas import CatCreate, CatUpdate, CatRead
from src.domain.cat.services import CatService

router = APIRouter(prefix='/cats', tags=['Cats'])

def get_service(db: Session = Depends(get_db)) -> CatService:
  return CatService(db)

@router.get('/', response_model=list[CatRead])
def list_cats(service: CatService = Depends(get_service)):
  return service.find_many()

@router.get('/{cat_id}', response_model=CatRead)
def get_cat(cat_id: int, service: CatService = Depends(get_service)):
  return service.get_by_id(cat_id)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CatRead)
def create_cat(data: CatCreate, service: CatService = Depends(get_service)):
  try:
    return service.create(data)
  except ValueError as e:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=str(e),
    )

@router.patch(
  '/{cat_id}/salary',
  summary='Update Cat Salary',
  response_model=CatUpdate
)
def update_cat(cat_id: int, data: CatUpdate, service: CatService = Depends(get_service)):
  return service.update(cat_id, data)

@router.delete('/{cat_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_cat(cat_id: int, service: CatService = Depends(get_service)):
  service.delete(cat_id)
