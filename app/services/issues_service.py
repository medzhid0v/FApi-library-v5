from sqlalchemy.orm import Session
from app.db.models import Issue, Book, Reader
from app.models.issue import IssueCreate


class IssueService:
    @staticmethod
    def get_all_issue(db: Session):
        """
        Получает список из базы данных.
        """
        return db.query(Issue).all()

    @staticmethod
    def create_issue(db: Session, issue_data: IssueCreate):
        """
        Создает новую выдачу книги читателю.
        """
        # Проверка, что книга существует и не выдана
        book = db.query(Book).filter(Book.id == issue_data.book_id).first()
        if not book:
            raise ValueError(f"Книга с ID {issue_data.book_id} не найдена")

        existing_issue = db.query(Issue).filter(Issue.book_id == issue_data.book_id).first()
        if existing_issue:
            raise ValueError(f"Книга с ID {issue_data.book_id} уже выдана")

        # Проверка, что читатель существует
        reader = db.query(Reader).filter(Reader.id == issue_data.reader_id).first()
        if not reader:
            raise ValueError(f"Читатель с ID {issue_data.reader_id} не найден")

        # Создание новой выдачи
        issue = Issue(**issue_data.dict())
        db.add(issue)
        db.commit()
        db.refresh(issue)
        return issue

    @staticmethod
    def get_issue(db: Session, issue_id: int):
        """
        Получает информацию о выдаче по её ID.
        """
        issue = db.query(Issue).filter(Issue.id == issue_id).first()
        if not issue:
            raise ValueError(f"Выдача с ID {issue_id} не найдена")
        return issue

    @staticmethod
    def get_all_issues(db: Session):
        """
        Возвращает список всех выдач.
        """
        return db.query(Issue).all()

    @staticmethod
    def delete_issue(db: Session, issue_id: int):
        """
        Закрывает выдачу, удаляя запись о ней (возврат книги).
        """
        issue = db.query(Issue).filter(Issue.id == issue_id).first()
        if not issue:
            raise ValueError(f"Выдача с ID {issue_id} не найдена")

        db.delete(issue)
        db.commit()
        return {"message": f"Выдача с ID {issue_id} закрыта"}
