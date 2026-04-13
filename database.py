from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
# from dotenv import load_dotenv

# postgresql
SQLALCHEMY_DATABASE_URL = 'postgresql://neondb_owner:npg_BPvL1YEn0qth@ep-spring-boat-alqpce46-pooler.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

# created the sqlite engine and opened multithred on sqlite to allow python
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
