import pytest
from sqlalchemy import create_engine, result_tuple
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text


# Класс для хранения состояние (любых данных) передающихся между тестами
class SharedData():
    def __init__(self, db):
        self.session = db  # сохраняем сессию к базе данных

    def get_session(self):
        return self.session


# Создаём фикстуру для базы данных
@pytest.fixture(scope="class")
def fixture_create_db(request):
    engine = create_engine("sqlite:///:memory:")  # используем бд в памяти
    SessionLocal = sessionmaker(bind=engine)

    session = SessionLocal()

    session.execute(text("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"))
    # Передаём сессию в тест
    request.cls.testData = SharedData(session)

    yield session

    session.close()  # Очистка после теста


@pytest.mark.usefixtures("fixture_create_db")
class TestSuite():
    def test_check_record(self):
        print("start test")
        # Используем фикстуру db_session
        session = self.testData.get_session()
        session.execute(text("INSERT INTO test (name) VALUES ('Alice')"))

        result = session.execute(text("SELECT * FROM test")).fetchall()
        assert len(result) == 1
        assert result[0][1] == "Alice"

    def test_count_records(self):
        session = self.testData.get_session()
        result = session.execute(text("SELECT * FROM test")).fetchall()
        assert len(result) == 3


