import re
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from fastapi import status
from datetime import timedelta, datetime, timezone
from jose import jwt
from pydantic import BaseModel
#from ..models.user.users import User
from ..constants.index import SECRET_KEY, HASHING_ALGORITHM

class User(BaseModel):
    username: str
    email: str
    inactive: bool

class UserInDB(User):
    hashed_password: str

# snippets for valid email
def email_check(email: str) -> ValueError | bool:
    if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
        raise ValueError("sorry email is not correct")
    return True

# below are written security code snippets
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# password verification using hashing algorithm
def verify_password(old_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(old_password, hashed_password)

# hash the user password using passlib package
def generate_hashed_password(password: str):
    return pwd_context.hash(password)

def verify_user_email(db, user_email: str) -> bool:
    if user_email not in db:
        return False
    return True

# a function which retrieve the user info
def retrieve_user_data(db, username: str):
    if username is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="sorry no user detected")
    if username in db:
        retrieve_user_dict = db[username]
        return UserInDB(**retrieve_user_dict)
                     
# method to retrieve authenticate user
def authenticate_user(db, username: str, password: str):
    user = retrieve_user_data(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# user access token logical creation
def create_access_token(data, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else: 
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_data = jwt.encode(to_encode, SECRET_KEY, algorithm=HASHING_ALGORITHM)
    return encoded_data

