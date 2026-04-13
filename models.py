import uuid
from typing import List
from sqlalchemy import DateTime, Uuid, func, String, ForeignKey
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_name: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)

    climbs: Mapped[List["Climb"]] = relationship(back_populates="user")


class Route(Base):
    __tablename__ = "routes"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50))
    grade: Mapped[str] = mapped_column(String(20))
    climbs: Mapped[List["Climb"]] = relationship(back_populates="route")


class Climb(Base):
    __tablename__ = "climbs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    route_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("routes.id"), index=True)


    is_sent: Mapped[bool] = mapped_column(default=False)
    attempts: Mapped[int] = mapped_column(default=1)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship(back_populates="climbs")
    route: Mapped["Route"] = relationship(back_populates="climbs")
