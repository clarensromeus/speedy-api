from fastapi import APIRouter, Path, status, Depends, Body, Query
from  fastapi.encoders import jsonable_encoder
from typing import Annotated
from fastapi.exceptions import HTTPException
from datetime import timedelta
from fastapi.security import  OAuth2PasswordRequestForm
import pendulum
from bson import ObjectId
# internally relative imports of ressources
from ...models.token.index import Token
from ...schema.users import userEmptity, usersEmptity
from ...Interface.user.user_interface import UserInterface
from ...depencies.user import  user_upload_file, retrieve_current_user
from ...models.user.user_base import User_Base
from ...enums.index import UserTags
from ...utils.user import  verify_password, generate_hashed_password
from ...utils.user import  create_access_token
from ...constants.index import ACCESS_TOKEN_EXPIRE_MINUTES
from ...models.user.users import User_Extra
from ...config.connection import db
from ...models.user.users import User
from ...models.user.response import Response


userRouter = APIRouter(prefix="/user")  

@userRouter.post("/login", tags=[UserTags.SINGLE_USER], summary="after the logged-in step you'll full access",
                 description="Login if you're already a member")
async def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    if not form_data.username or not form_data.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="sorry no information provided")
    user_data = await db.users.find_one({"username": form_data.username})
    # check if there's a user which goes by that username, if not throw an http exception error
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # check if user is authenticated, if not throw an http exception error
    user_password_verification = verify_password(form_data.password, user_data["hashed_password"])
    if not user_password_verification:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    user_access_token = create_access_token({"sub": form_data.username}, access_token_expires)
    return Token(access_token=user_access_token, token_type="bearer")

    
@userRouter.post("/register", status_code=status.HTTP_201_CREATED, response_model="",
                 tags=[UserTags.SINGLE_USER], description="registered in the platform for a membership")
async def user_register(user_input: User_Base, passcode: Annotated[User_Extra,
                                                                   Body(embed=True, description="user password")]):                                                                             

    user = await db.users.find_one({"username": user_input.username, "email": user_input.email})
    if user is not None:
        user_password = verify_password(old_password=passcode.password, hashed_password=user.hashed_password)
        if user_password is not None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="sorry user already registered")
    try:
        user_hashed_password = generate_hashed_password(password=passcode.password)
        user_data_to_insert = User(**dict(user_input), hashed_password=user_hashed_password, date_joined=pendulum.now(tz="America/Port-au-prince"))
        user_creation = await db.users.insert_one(user_data_to_insert.model_dump(mode="json"))
        user_data_update = user_data_to_insert.model_copy(update={"_id": str(user_creation.inserted_id)})
        encode_user_data = jsonable_encoder(user_data_update)
        if not user_creation.acknowledged:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="sorry something went wrong with your info")         
        return encode_user_data
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error)
 
 
@userRouter.patch("/upload", response_model=User, description="capability of user uploading image",
                status_code=status.HTTP_200_OK, tags=[UserTags.SINGLE_USER])
async def upload_user_image(current_user: Annotated[UserInterface, Depends(retrieve_current_user)],
                        user_image_url: Annotated[str, Depends(user_upload_file)]):
    if not user_image_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bad credentials")
    user_data = await db.users.find_one_and_update({"_id": ObjectId(current_user["_id"])}, {"$set": {"pictured_url": user_image_url}})
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bad credentials")
    serialize_user = userEmptity(user_data)
    return serialize_user
    

@userRouter.get("/allusers/", status_code=status.HTTP_200_OK, tags=[UserTags.ALL_USER],
                description="a list of all users on the platform", response_model=list[User])
async def retrieve_all_users(limit: Annotated[int, Query(gt=0, lt=101, title="LIMIT_NUMBER")]):
    users = await  db.users.find().to_list(length=limit)
    if not users or len(users) <= 0:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No content")
    serialize_users = usersEmptity(users)
    return serialize_users


@userRouter.get("/one_user", response_model=User, status_code=status.HTTP_201_CREATED,
                tags=[UserTags.SINGLE_USER], description="unique information of a single user")
async def one_user(current_user: Annotated[UserInterface, Depends(retrieve_current_user)]):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    serialize_user = userEmptity(current_user)
    return serialize_user

    
@userRouter.put("/update_user", status_code=status.HTTP_200_OK, response_model=User,
                description="information of a single user", tags=[UserTags.SINGLE_USER])
async def update_user(current_user: Annotated[UserInterface, Depends(retrieve_current_user)], 
                      user_info: User_Base):
    print(current_user["_id"])
    user_data = await db.users.find_one({"_id": ObjectId(current_user["_id"])})
    if not user_data:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Sorry, bad request")
    try:
        data_filtering = user_info.model_dump(exclude_unset=True, exclude_none=True, mode="json")
        update_user_data = await db.users.find_one_and_update({"_id": ObjectId(current_user["_id"])}, {"$set": data_filtering})
        serialize_user = userEmptity(update_user_data)
        return serialize_user
    except Exception as error:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error)
    
    
@userRouter.delete("/{user_id}", status_code=status.HTTP_202_ACCEPTED, description="deleting user from the platform",
                   tags=[UserTags.SINGLE_USER])
async def delete_user(user_id: Annotated[str, Path(max_length=50, min_length=6, title="USER_ID")]) -> Response:
    user = await db.users.find_one_and_delete({"_id": user_id}) 
    if user is None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="sorry, bad request")
    return Response(message=f"deleted user {user.usernane} with success", success=True)
