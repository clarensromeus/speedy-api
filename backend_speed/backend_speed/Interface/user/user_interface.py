from typing import Annotated
from annotated_types import Predicate
from .user_base import UserBase
from ..product.product_base import ProductBase

class UserInterface(UserBase):
    _id: Annotated[str, Predicate(str.isidentifier)]
    products: list[ProductBase] | None
    pictured_url: Annotated[str, Predicate(str.isalnum)]