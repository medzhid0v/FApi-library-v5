from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.books_service import BookService
from app.db.session import get_db
from app.models.book import BookCreate, BookResponse
from typing import List

router = APIRouter()


@router.get("/", response_model=List[BookResponse])
async def get_all_books(db: Session = Depends(get_db)):
    try:
        return BookService.get_all_books(db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=BookResponse)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    try:
        return BookService.create_book(db, book)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}", response_model=BookResponse)
async def get_book(id: int, db: Session = Depends(get_db)):
    try:
        book = BookService.get_book(db, id)
        if not book:
            raise ValueError(f"Книга {id} не найдена")
        return book
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}")
async def delete_book(id: int, db: Session = Depends(get_db)):
    try:
        return BookService.delete_book(db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
