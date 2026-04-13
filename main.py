from typing import Sequence
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import select, Select, desc
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_index():
    return FileResponse("static/index.html")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")

# # Endpoints
# def seed_grades(db: Session):
#     # Check if we already have grades
#     if db.query(models.Grade).first():
#         return
#
#     # Add Bouldering Grades
#     v_grades = ["V0", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V11", "V12", "V13", "V14", "V15", "V16"]
#     for i, val in enumerate(v_grades):
#         db.add(models.BoulderingGrade(value=val, rank=i))
#
#     # Add Sport Grades
#     s_grades = ["5.8", "5.9", "5.10a", "5.10b", "5.11a"]
#     for i, val in enumerate(s_grades):
#         db.add(models.SportGrade(value=val, rank=i))
#
#     db.commit()
#
# @app.post("/climbs/", response_model=schemas.ClimbResponse)
# def create_climb(climb: schemas.ClimbCreate, db: Session = Depends(get_db)):
#     db_climb: models.Climb | None = None
#     stmt = select(models.Climb).where(
#         models.Climb.name == climb.name, models.Climb.grade == climb.grade
#     )
#     existing_climb: models.Climb | None = db.execute(stmt).scalar_one_or_none()
#
#     if existing_climb:
#         if existing_climb.is_sent:
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"You already sent '{climb.name}' ({climb.grade})",
#             )
#         existing_climb.attempts += 1
#         if climb.is_sent:
#             existing_climb.is_sent = True
#         db_climb = existing_climb
#     else:
#         new_climb = models.Climb(
#             name=climb.name, grade=climb.grade, is_sent=climb.is_sent, attempts=1
#         )
#         db.add(new_climb)
#         db_climb = new_climb
#
#     db.commit()
#     db.refresh(db_climb)
#     return db_climb
#
#
# @app.get("/climbs/", response_model=list[schemas.ClimbResponse])
# def read_climb(
#     skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
# ) -> Sequence[models.Climb]:
#     stmt: Select = (
#         select(models.Climb)
#         .order_by(desc(models.Climb.updated_at))
#         .offset(skip)
#         .limit(limit)
#     )
#     climbs: Sequence[models.Climb] = db.execute(stmt).scalars().all()
#     return climbs
#
# @app.get("/grades/", response_model=list[schemas.GradeResponse])
# def get_all_grades(type: str | None = None, db: Session = Depends(get_db)):
#     if type == "bouldering":
#         return db.query(models.BoulderingGrade).order_by(models.BoulderingGrade.rank).all()
#     elif type == "sport":
#         return db.query(models.SportGrade).order_by(models.SportGrade.rank).all()
#     return db.query(models.Grade).order_by(models.Grade.rank).all()
#
# @app.get("/climbs/sent/", response_model=list[schemas.ClimbResponse])
# def read_sent_climbs(
#     skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
# ) -> Sequence[models.Climb]:
#     stmt: Select = (
#         select(models.Climb)
#         .where(models.Climb.is_sent)
#         .order_by(desc(models.Climb.updated_at))
#         .offset(skip)
#         .limit(limit)
#     )
#
#     results: Sequence[models.Climb] = db.execute(stmt).scalars().all()
#     return results
