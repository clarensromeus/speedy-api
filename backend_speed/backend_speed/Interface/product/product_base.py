# external imports
from annotated_types import Gt, Lt, Predicate , Len, Timezone, MaxLen
from typing import Annotated, TypedDict
from datetime import datetime
import math
from decimal import Decimal
# internally relative imports
from ..sale.sale_interface import Sale_interface

class ProductBase(TypedDict):
    product_name: Annotated[str, Len(min_length=5, max_length=20), Predicate(str.isalpha)]
    product_description: Annotated[str | None, Len(min_length=7, max_length=30), Predicate(str.isalpha)]
    price: Annotated[Decimal, Lt(5000.999), Gt(100.00), Predicate(str.isdecimal), Predicate(math.isnan)]
    sales: list[Sale_interface]
    date_created: Annotated[datetime, Timezone("America/Port-au-prince")]
    date_updated: Annotated[datetime, Timezone("America/Port-au-prince")]  