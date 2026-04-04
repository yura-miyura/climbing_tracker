from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ClimbBase(BaseModel):
    name: str
    grade: str
    is_sent: bool = False
    attempts: int = 1

class ClimbCreate(ClimbBase):
    pass

class ClimbResponse(ClimbBase):
    id: int
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
