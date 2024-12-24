import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.db.session import get_db
from app.db.models import Base

test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
SessionLocal = sessionmaker(bind=test_engine)

Base.metadata.create_all(bind=test_engine)

def override_get_db():
    """Подменяем зависимость для использования тестовой базы."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_book():
    response = client.post("/book/", json={"title": "Грокаем Алгоритмы", "author": "Тестовый автор "})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Грокаем Алгоритмы"
    assert data["author"] == "Тестовый автор "

    list_response = client.get("/book/")
    assert list_response.status_code == 200
    books = list_response.json()
    assert any(book["title"] == "Грокаем Алгоритмы" for book in books)

def test_get_book():
    create_response = client.post("/book/", json={"title": "1984", "author": "Дж. Оруэлл"})
    assert create_response.status_code == 200
    created_book = create_response.json()
    book_id = created_book["id"]

    response = client.get(f"/book/{book_id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == book_id
    assert data["title"] == "1984"
    assert data["author"] == "Дж. Оруэлл"

def test_delete_book():
    create_response = client.post("/book/", json={"title": "Война и мир", "author": "Л. Толстой"})
    assert create_response.status_code == 200
    created_book = create_response.json()
    book_id = created_book["id"]

    delete_response = client.delete(f"/books/{book_id}/")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": f"Книга с ID {book_id} удалена"}

    get_response = client.get(f"/books/{book_id}/")
    assert get_response.status_code == 404

    list_response = client.get("/book/")
    books = list_response.json()
    assert not any(book["id"] == book_id for book in books)

def test_get_all_books():
    client.post("/book/", json={"title": "Книга 1", "author": "Автор 1"})
    client.post("/book/", json={"title": "Книга 2", "author": "Автор 2"})

    response = client.get("/book/")
    assert response.status_code == 200
    books = response.json()
    assert len(books) >= 2
    assert any(book["title"] == "Книга 1" for book in books)
    assert any(book["title"] == "Книга 2" for book in books)
