from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError
from passlib.context import CryptContext

SECRET_KEY = "bf27c34a99a7246b8a653f8340e6bfe3509eb80837d557b68cb2e1b6f6922c5bed1c54ed46050ac67311c09c19c95d409172176d21109e42b9a140ac776f177b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if(expires_delta):
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expires})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decode_token.get("userid")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    userid = payload
    if userid is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    return userid

