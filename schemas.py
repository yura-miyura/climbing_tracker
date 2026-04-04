from pydantic import BaseModel, ConfigDict

class ClimbBase(BaseModel):
    name: str
    grade: str
    is_sent:bool = False

class ClimbCreate(ClimbBase):
    pass

class ClimbResponse(ClimbBase):
    id: int
    attempts: int

    model_config = ConfigDict(from_attributes=True)
