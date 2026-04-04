from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.schema import SchemaVisitable
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

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
    existing_sent_climb = None
    if climb.is_sent:
        existing_sent_climb = db.query(models.Climb).filter(
                models.Climb.name == climb.name,
                models.Climb.grade == climb.grade,
                models.Climb.is_sent
                ).first()
    if existing_sent_climb:
        raise HTTPException(
                status_code=400,
                detail=f"You already logged '{climb.name}' ({climb.grade}) as is_sent: {climb.is_sent}"
                )
    db_climb = models.Climb(name=climb.name, grade=climb.grade, is_sent=climb.is_sent)
    db.add(db_climb)
    db.commit()
    db.refresh(db_climb)
    return db_climb

@app.get("/climbs/", response_model=list[schemas.ClimbResponse])
def read_climb(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    climbs = db.query(models.Climb).offset(skip).limit(limit).all()
    return climbs

@app.get("/climbs/sent/", response_model=list[schemas.ClimbResponse])
def read_sent_climbs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    climbs = db.query(models.Climb).filter(models.Climb.is_sent).offset(skip).limit(limit).all()
    return climbs
