from pydantic import Field
from datetime import datetime
from typing import Annotated
from .sales import Sale_Base

class SaleOuput(Sale_Base):
    product: Annotated[str, Field(default="COCA-COLA", max_length=30, min_length=5, 
                                       validate_default=True, description="PRODUCT_NAME", strict=True)]
    date_selling: datetime = Field(...)
    