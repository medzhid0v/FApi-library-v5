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


def test_create_issue():
    book_response = client.post("/book/", json={"title": "Анна Каренина", "author": "Л. Толстой"})
    assert book_response.status_code == 200
    book_id = book_response.json()["id"]

    reader_response = client.post("/reader/", json={"name": "Александр"})
    assert reader_response.status_code == 200
    reader_id = reader_response.json()["id"]

    issue_response = client.post("/issue/", json={"book_id": book_id, "reader_id": reader_id})
    assert issue_response.status_code == 200
    issue_data = issue_response.json()
    assert issue_data["book_id"] == book_id
    assert issue_data["reader_id"] == reader_id


def test_get_issue():
    book_response = client.post("/book/", json={"title": "Преступление и наказание", "author": "Ф. Достоевский"})
    assert book_response.status_code == 200
    book_id = book_response.json()["id"]

    reader_response = client.post("/reader/", json={"name": "Мария"})
    assert reader_response.status_code == 200
    reader_id = reader_response.json()["id"]

    issue_response = client.post("/issue/", json={"book_id": book_id, "reader_id": reader_id})
    assert issue_response.status_code == 200
    issue_id = issue_response.json()["id"]

    get_response = client.get(f"/issue/{issue_id}/")
    assert get_response.status_code == 200
    issue_data = get_response.json()
    assert issue_data["id"] == issue_id
    assert issue_data["book_id"] == book_id
    assert issue_data["reader_id"] == reader_id


# Тест закрытия выдачи
def test_close_issue():
    book_response = client.post("/book/", json={"title": "Обломов", "author": "И. Гончаров"})
    assert book_response.status_code == 200
    book_id = book_response.json()["id"]

    reader_response = client.post("/reader/", json={"name": "Олег"})
    assert reader_response.status_code == 200
    reader_id = reader_response.json()["id"]

    issue_response = client.post("/issue/", json={"book_id": book_id, "reader_id": reader_id})
    assert issue_response.status_code == 200
    issue_id = issue_response.json()["id"]

    delete_response = client.delete(f"/issue/{issue_id}/")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": f"Выдача с ID {issue_id} закрыта"}

    get_response = client.get(f"/issue/{issue_id}/")
    assert get_response.status_code == 404


def test_get_all_issues():
    book1_response = client.post("/book/", json={"title": "Дети капитана Гранта", "author": "Ж. Верн"})
    assert book1_response.status_code == 200
    book1_id = book1_response.json()["id"]

    reader1_response = client.post("/reader/", json={"name": "Елена"})
    assert reader1_response.status_code == 200
    reader1_id = reader1_response.json()["id"]

    book2_response = client.post("/book/", json={"title": "Три мушкетера", "author": "А. Дюма"})
    assert book2_response.status_code == 200
    book2_id = book2_response.json()["id"]

    reader2_response = client.post("/reader/", json={"name": "Дмитрий"})
    assert reader2_response.status_code == 200
    reader2_id = reader2_response.json()["id"]

    client.post("/issue/", json={"book_id": book1_id, "reader_id": reader1_id})
    client.post("/issue/", json={"book_id": book2_id, "reader_id": reader2_id})

    list_response = client.get("/issue/")
    assert list_response.status_code == 200
    issues = list_response.json()
    assert len(issues) >= 2
    assert any(issue["book_id"] == book1_id and issue["reader_id"] == reader1_id for issue in issues)
    assert any(issue["book_id"] == book2_id and issue["reader_id"] == reader2_id for issue in issues)
