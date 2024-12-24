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

def test_create_reader():
    response = client.post("/reader/", json={"name": "Маргарита"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Маргарита"

    list_response = client.get("/reader/")
    assert list_response.status_code == 200
    readers = list_response.json()
    assert any(reader["name"] == "Маргарита" for reader in readers)

def test_get_reader():
    create_response = client.post("/reader/", json={"name": "Николай"})
    assert create_response.status_code == 200
    created_reader = create_response.json()
    reader_id = created_reader["id"]

    response = client.get(f"/reader/{reader_id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == reader_id
    assert data["name"] == "Николай"

def test_delete_reader():
    create_response = client.post("/reader/", json={"name": "Сергей"})
    assert create_response.status_code == 200
    created_reader = create_response.json()
    reader_id = created_reader["id"]

    delete_response = client.delete(f"/reader/{reader_id}/")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": f"Читатель с ID {reader_id} удалён"}

    get_response = client.get(f"/reader/{reader_id}/")
    assert get_response.status_code == 404

    list_response = client.get("/reader/")
    readers = list_response.json()
    assert not any(reader["id"] == reader_id for reader in readers)

def test_get_all_readers():
    client.post("/reader/", json={"name": "Георгий"})
    client.post("/reader/", json={"name": "Ольга"})

    response = client.get("/reader/")
    assert response.status_code == 200
    readers = response.json()
    assert len(readers) >= 2
    assert any(reader["name"] == "Георгий" for reader in readers)
    assert any(reader["name"] == "Ольга" for reader in readers)
