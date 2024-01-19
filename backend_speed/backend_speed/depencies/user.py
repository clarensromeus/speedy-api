from fastapi.exceptions import HTTPException
from fastapi import Depends, status, UploadFile, File
from typing import Annotated
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
import secrets
import os
# internally relative imports of resources
from ..constants.index import SECRET_KEY, HASHING_ALGORITHM, NUMBER_OF_BYTES, UPLOAD_DIR, PROJECT_HOST, PROJECT_PROTOCOLE
from ..models.token.index import TokenData
from ..config.settings import GET_SETTINGS
from ..config.connection import db
from ..schema.users import userEmptity

settings = GET_SETTINGS()

# this line of code contains the the url whose token will be created from a client credentials
oauth_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

async def retrieve_current_user(token: Annotated[str, Depends(oauth_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
        
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASHING_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data: TokenData = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await db.users.find_one({"username": token_data.username})
    if user is None:
        raise credentials_exception
    return userEmptity(user)

# method handler for uploading file
async def user_upload_file(file: Annotated[UploadFile, File(...)]):
    if file.filename:
        f_name, f_ext = file.filename.split(".")
        # first off recover the original file name and chop out name and extension separately
        unique_file_name = "{0}-{1}.{2}".format(secrets.token_hex(NUMBER_OF_BYTES), f_name, f_ext)
        FILE_SAVING_DESTINATION = os.path.join(UPLOAD_DIR, unique_file_name)
        with open(FILE_SAVING_DESTINATION, "wb") as f:
            # recover the file bytes
            file_bytes = await file.read()
            # write the file bytes into the upload directory
            f.write(file_bytes)
        IMAGE_URL = "{0}://{1}:{2}/static/{3}".format(PROJECT_PROTOCOLE, PROJECT_HOST, settings["PROJECT_PORT"], unique_file_name)
        return IMAGE_URL
            
    
    
    
    