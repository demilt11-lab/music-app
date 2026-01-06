from typing import Generator
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
import os
from sqlalchemy.orm import Session
from database import SessionLocal
import crud, schemas, models
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
ALGORITHM = "HS256"

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(lambda: None), db: Session = Depends(get_db)):
    # Keep it simple: FastAPI will supply token from header via oauth2 scheme in main.py
    raise NotImplementedError("Use the dependency in main.py where OAuth2PasswordBearer is defined.")
