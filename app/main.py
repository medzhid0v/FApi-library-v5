from fastapi import FastAPI
from app.api import books, readers, issues
from app.db.base import init_db

app = FastAPI(
    title="Library API",
    description="API для управления библиотекой",
    version="1.0.0"
)

# Подключение маршрутов
app.include_router(books.router, prefix="/book", tags=["Books"])
app.include_router(readers.router, prefix="/reader", tags=["Readers"])
app.include_router(issues.router, prefix="/issue", tags=["Issues"])


# Инициализация базы данных при старте приложения
@app.on_event("startup")
async def startup():
    init_db()


@app.on_event("shutdown")
async def shutdown():
    print("Application is shutting down...")
