from .statements import get_pwd
from .database import SessionLocal
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.hash import sha256_crypt

security = HTTPBasic()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# authentication
def authentication(credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db)):

    username = credentials.username
    password = credentials.password

    # password stored for a given user
    try:
        pwd_stored = get_pwd(db, username).pwd_hashed
    except AttributeError:
        # raising exception if invalid credentials were supplied
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid ID",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    # verifying password
    logged = sha256_crypt.verify(password, pwd_stored)

    if logged:
        return username
    else:
        # raising exception if invalid credentials were supplied
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )