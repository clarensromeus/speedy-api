from typing import Annotated
from pydantic import Field, BaseModel, field_validator, PrivateAttr
from .user_base import User_Base
from ..product.product_base import Product_Base
import re
from datetime import datetime

class User(User_Base):
    _id: str | None = PrivateAttr(default=None)
    date_joined: datetime = Field(...)
    hashed_password: Annotated[str, Field(default="Jhonny(+-1998)", max_length=60, min_length=8),]
    products: list[Product_Base] = Field(default_factory=lambda: [])
    
class User_Extra(BaseModel):
    password: Annotated[str, Field(default="Jhonny(+-1998)", max_length=60, min_length=8, pattern=r'')]
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str)-> ValueError | str:
       if not re.fullmatch(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$", password):
           raise ValueError("sorry, enter a strong password")
       return password
    