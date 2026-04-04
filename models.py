from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Climb(Base):
    __tablename__ = "climbs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    grade: Mapped[str] = mapped_column(index=True)
    is_sent: Mapped[bool] = mapped_column(default=False)
    attempts: Mapped[int] = mapped_column(default=1)
