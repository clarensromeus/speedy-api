from typing import Annotated
from annotated_types import Predicate, MaxLen
from .product_base import ProductBase
from ..user.user_base import UserBase

class Product(ProductBase):
    _id: Annotated[str, Predicate(str.isalpha), MaxLen(50), Predicate(str.isidentifier)]
    owner: UserBase
    