import uuid
from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    user_name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=72)


class UserResponse(UserBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class RouteBase(BaseModel):
    name: str
    grade: str


class RouteCreate(RouteBase):
    pass


class RouteResponse(RouteBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class ClimbBase(BaseModel):
    is_sent: bool = False
    attempts: int = 1


class ClimbCreate(ClimbBase):
    user_id: uuid.UUID
    route_id: uuid.UUID


class ClimbResponse(ClimbBase):
    id: uuid.UUID
    updated_at: datetime

    route: RouteResponse

    model_config = ConfigDict(from_attributes=True)


class UserWithClimbs(UserResponse):
    climbs: List[ClimbResponse]
