from pydantic import BaseModel

class IssueBase(BaseModel):
    book_id: int
    reader_id: int

class IssueCreate(IssueBase):
    pass

class IssueResponse(IssueBase):
    id: int

    class Config:
        from_attributes  = True
