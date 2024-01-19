from annotated_types import Len, Predicate, Gt, Lt, IsNotNan, Timezone
import math
from typing import Annotated, TypedDict
from datetime import datetime

class Sale_base(TypedDict):
    product: Annotated[str, Len(min_length=5, max_length=20), IsNotNan, Predicate(str.isalpha)]
    quantity: Annotated[int, Lt(100), Gt(0), IsNotNan, Predicate(math.isinf), Predicate(str.isdigit)]
    date_selling: Annotated[datetime, Timezone("America/Port-au-prince")]
