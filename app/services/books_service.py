from sqlalchemy.orm import Session
from app.db.models import Book
from app.models.book import BookCreate


class BookService:
    @staticmethod
    def get_all_books(db: Session):
        return db.query(Book).all()

    @staticmethod
    def create_book(db: Session, book_data: BookCreate):
        book = Book(**book_data.model_dump())
        db.add(book)
        db.commit()
        db.refresh(book)
        return book

    @staticmethod
    def get_book(db: Session, book_id: int):
        return db.query(Book).filter(Book.id == book_id).first()

    @staticmethod
    def delete_book(db: Session, book_id: int):
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise ValueError(f"Книга с ID {book_id} не найдена!")

        db.delete(book)
        db.commit()
        return {"message": f"Книга с ID {book_id} удалена!"}
