import uuid
from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    user_name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


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
