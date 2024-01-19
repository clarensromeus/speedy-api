from fastapi import FastAPI, Query, HTTPException, status
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from typing import Annotated
# internally relative imports or ressources
from .config.settings import GET_SETTINGS
from .routers.users.user import userRouter
from .enums.index import MemberRole
from .config.connection import db
from .schema.users import usersEmptity
from .routers.products.product import productRouter
from .routers.sales.sale import saleRouter
from .models.user.users import User

Server: FastAPI = FastAPI()

setting = GET_SETTINGS()

# include user router features in 
Server.include_router(userRouter)
# include product router features in
Server.include_router(productRouter)
# include sale router features in
Server.include_router(saleRouter)

# mounting a static path to upload images
Server.mount("/static", StaticFiles(directory=os.path.join("backend_speed", "Uploads")), name="uploads")

@Server.get("/{member_role}", tags=["ROLE"], response_model=list[User])
async def launch(member_role: MemberRole, limit: Annotated[int, Query(..., gt=4, lt=20, strict=True, 
                                                                      title="number of administrator to record from", description="LIMIT_OF_NUMBER")]):
    # grab all administrators from the platform
    administrators = await db.users.find({"role": member_role.value}).to_list(length=limit)
    if member_role not in MemberRole or member_role.value != "ADMINISTRATOR":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sorry, bad request")
    if administrators is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="no content registered")
    serialize_user = usersEmptity(administrators)
    return serialize_user
# method to start the application server        
def start_server():
    uvicorn.run("backend_speed.run:Server", host=setting["DATABASE_HOST"], port=setting["PROJECT_PORT"], reload=setting["PROJECT_RELOADING"])