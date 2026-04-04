from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Climb(Base):
    __tablename__ = "climbs"

    id = Column(Integer, primary_key= True, index=True)
    name = Column(String, index=True)
    grade = Column(String, index=True)
    is_sent = Column(Boolean, default=False)
