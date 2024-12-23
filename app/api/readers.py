from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.readers_service import ReaderService
from app.db.session import get_db
from app.models.reader import ReaderCreate, ReaderResponse
from typing import List

router = APIRouter()


@router.get("/", response_model=List[ReaderResponse])
async def get_all_reader(db: Session = Depends(get_db)):
    try:
        return ReaderService.get_all_reader(db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=ReaderResponse)
async def create_reader(reader: ReaderCreate, db: Session = Depends(get_db)):
    """
    Создать читателя
    """
    try:
        return ReaderService.create_reader(db, reader)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}", response_model=ReaderResponse)
async def get_reader(id: int, db: Session = Depends(get_db)):
    """
    Получить информацию о читателе
    """
    try:
        return ReaderService.get_reader(db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}")
async def delete_reader(id: int, db: Session = Depends(get_db)):
    """
    Удалить читателя
    """
    try:
        return ReaderService.delete_reader(db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
