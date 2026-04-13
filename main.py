import uuid
from datetime import datetime, timedelta
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select
from jose import JWTError, jwt
from passlib.context import CryptContext

import models
import schemas
from database import SessionLocal, engine

# --- SECURITY CONFIG ---
SECRET_KEY = "YOUR_SUPER_SECRET_KEY_KEEP_IT_SAFE" # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- DATABASE SETUP ---
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# MOUNT STATIC FILES: This allows http://127.0.0.1:8000/static/index.html to work
app.mount("/static", StaticFiles(directory="static"), name="static")
# If you kept images separate:
app.mount("/images", StaticFiles(directory="images"), name="images")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- HELPER FUNCTIONS ---
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- 1. AUTH & USER ENDPOINTS ---

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm uses 'username' field, which we treat as email
    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id}

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # DEBUG: See what is actually being sent to the hasher
    print(f"DEBUG: Password length is {len(user.password)}")

    # HASH THE PASSWORD before saving
    hashed_pwd = pwd_context.hash(user.password)

    new_user = models.User(
        user_name=user.user_name,
        email=user.email,
        hashed_password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# --- 2. ROUTE & CLIMB ENDPOINTS ---

@app.post("/routes/", response_model=schemas.RouteResponse)
def create_route(route: schemas.RouteCreate, db: Session = Depends(get_db)):
    # Check if route already exists to avoid duplicates
    existing = db.query(models.Route).filter(
        models.Route.name == route.name,
        models.Route.grade == route.grade
    ).first()
    if existing:
        return existing

    new_route = models.Route(**route.model_dump())
    db.add(new_route)
    db.commit()
    db.refresh(new_route)
    return new_route

@app.post("/climbs/", response_model=schemas.ClimbResponse)
def log_climb(climb: schemas.ClimbCreate, db: Session = Depends(get_db)):
    user = db.get(models.User, climb.user_id)
    route = db.get(models.Route, climb.route_id)

    if not user or not route:
        raise HTTPException(status_code=404, detail="User or Route not found")

    stmt = select(models.Climb).where(
        models.Climb.user_id == climb.user_id,
        models.Climb.route_id == climb.route_id
    )
    existing_climb = db.execute(stmt).scalars().first()

    if existing_climb:
        existing_climb.attempts += 1
        existing_climb.is_sent = climb.is_sent
        db.commit()
        db.refresh(existing_climb)
        return existing_climb

    new_climb = models.Climb(**climb.model_dump())
    db.add(new_climb)
    db.commit()
    db.refresh(new_climb)
    return new_climb

@app.get("/users/{user_id}/logbook", response_model=List[schemas.ClimbResponse])
def get_user_logbook(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.climbs

# --- 3. ROOT REDIRECT (Convenience) ---
@app.get("/")
async def read_index():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/static/index.html")
