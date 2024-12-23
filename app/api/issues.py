from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.issues_service import IssueService
from app.db.session import get_db
from app.models.issue import IssueCreate, IssueResponse
from typing import List

router = APIRouter()


@router.get("/", response_model=List[IssueResponse])
async def get_all_issue(db: Session = Depends(get_db)):
    try:
        return IssueService.get_all_issue(db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=IssueResponse)
async def create_issue(issue: IssueCreate, db: Session = Depends(get_db)):
    """
    Создать выдачу книги читателю
    """
    try:
        return IssueService.create_issue(db, issue)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}", response_model=IssueResponse)
async def get_issue(id: int, db: Session = Depends(get_db)):
    """
    Получить информацию о выдаче
    """
    try:
        return IssueService.get_issue(db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}")
async def delete_issue(id: int, db: Session = Depends(get_db)):
    """
    Закрыть выдачу (вернуть книгу)
    """
    try:
        return IssueService.delete_issue(db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
