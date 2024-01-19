from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Annotated
from decimal import Decimal


class Product_Base(BaseModel):
    product_name: Annotated[str, Field(default="COCA-COLA", max_length=30, min_length=5, 
                                       validate_default=True, description="PRODUCT_NAME")]
    product_description: Annotated[str, Field("Good quality product", max_length=50, min_length=10)]
    price: Annotated[int, Field(ge=100, le=5000, description="PRODUCT_PRICE")] | None = None
    
    model_config = ConfigDict(populate_by_name=True, validate_assignment=True,
                              revalidate_instances="always", json_schema_extra={
                                  "product_name": "COCA-COLA",
                                  "product_description": "Good quality product",
                                  "price": 100.00,
                                  "owner": {
                                        "username": "Jhonnyrodgelin",
                                        "password": "Jhonny(+-1998)",
                                        "email": "Jhonnyrodgelin202@gamil.com",
                                        "joined_at": "2024-01-12T17:57:01.819189-05:00",
                                        "proffession": "COMPUTER SCIENCE",
                                  },
                                  "sales": [
                                    {
                                        "product": "COCA-COLA",
                                        "quantity": 2
                                    },
                                    {
                                        "product": "NATURAL JUICE",
                                        "quantity": 39
                                    }
                                ],
                                  "date_created": "2024-01-12T17:57:01.819189-05:00",
                                  "date_updated": "2024-01-12T17:57:01.819189-05:00",
                              })