from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal, engine

models.Base.meradata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints

@app.post("/climbs/", response_model=schemas.ClimbResponse)
def create_climb(climb: schemas.ClimbCreate, db: Session = Depends(get_db)):
    db_climb = models.Climb(name=climb.name, grade=climb.grade, is_sent=climb.is_sent)
    db.add(db_climb)
    db.commit()
    db.refresh(db_climb)
    return db_climb

@app.get("/climbs/", response_model=list[schemas.ClimbResponse])
def read_climb(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    climbs = db.query(models.Climb).offset(skip).limit(limit).all()
    return climbs
