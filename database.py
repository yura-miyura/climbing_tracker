from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# lite locat database
SQLALCHEMY_DATABASE_URL = "sqlite:///./bouldering.db"

# created the sqlite engine and opened multithred on sqlite to allow python
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
