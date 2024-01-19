from pydantic import BaseModel, ConfigDict, StrictInt, Field, PrivateAttr
from datetime import datetime
from typing import Annotated
from datetime import datetime
import secrets




class Sale_Base(BaseModel):
    quantity: StrictInt = Field(..., lt=100, gt=0, validate_default=True)
    #date_selling: datetime = Field(...)
    
    model_config = ConfigDict(populate_by_name=True, extra="forbid", revalidate_instances="always",
                              validate_assignment=True, json_schema_extra={
                                  "product": "COCA-COLA",
                                  "quantity": 100,
                                  "date_selling": "2024-01-12T17:57:01.819189-05:00"
                              })

    
    