from typing import Annotated
from annotated_types import Predicate
from .sale_base import Sale_base

class Sale_interface(Sale_base):
    _id: Annotated[str, Predicate(str.isalnum), Predicate(str.isidentifier)]