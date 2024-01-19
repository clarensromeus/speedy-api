from pydantic import Field, PrivateAttr
from datetime import datetime
from .product_base import Product_Base
from ..user.user_base import User_Base
from ...models.sale.saleOuput import SaleOuput


class Product(Product_Base):
    _id: str | None = PrivateAttr(default=None)
    owner: User_Base = Field(default_factory=lambda: dict)
    sales: list[SaleOuput] = Field(default_factory=lambda: [])
    date_created: datetime = Field(...)
    date_updated: datetime = Field(...)