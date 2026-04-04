from pydantic import BaseModel

class ClimbBase(BaseModel):
    name: str
    grade: str
    is_sent:bool = False

class ClimbCreate(ClimbBase):
    pass

class ClimbResponse(ClimbBase):
    id: int

    class Config:
        orm_mode = True
