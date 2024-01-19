from pydantic import (BaseModel, ConfigDict, Field, StrictFloat, EmailStr, AliasChoices, HttpUrl)
from typing import Annotated
from ...enums.index import MemberRole


class User_Base(BaseModel):
    username: Annotated[str, Field(default="Jhonnyrodgelin", strict=True, validate_default=True, 
                                   min_length=5, max_length=50, title="username information", description="USERNAME")]
    email: Annotated[EmailStr, Field(default="Jhonnyrodgelin202@gmail.com", description="USERNAME",
                                     validate_default=True, title="user email information")]
    networth: StrictFloat = Field(100.00, gt=99, lt=50000.99, title="user lifetime networth", description="NETWORTH")
    proffession: Annotated[str, Field(default="computer science", validate_default=True, 
                                      validation_alias=AliasChoices("COMPUTER SIENCE", "CONTENT CREATOR", "ONLINE PRODUCER", "BUSINESSMAN"))]
    role: MemberRole = MemberRole.GUEST
    pictured_url: HttpUrl | None = None
    model_config = ConfigDict(populate_by_name=True, validation_error_cause=True,
                              validate_assignment=True, revalidate_instances="always",
                              json_schema_extra={
                                  "username": "Jhonnyrodgelin",
                                  "email": "Jhonnyrodgelin202@gmail.com",
                                  "networth": 400.449,
                                  "proffession": "COMPUTER SCIENCE",
                                  "role": "GUEST",
                                  "products": [
                                      {
                                          "product_name": "COCA-COLA",
                                          "product_description": "Good quality product",
                                          "sale": [
                                            {
                                                "product": "COCA-COLA", 
                                                "quantity": 12,
                                                "date_selling": "2024-01-12T17:57:01.819189-05:00"
                                              
                                            }
                                          ],
                                          "date_created": "2024-01-12T17:57:01.819189-05:00",
                                          "date_updated": "2024-01-12T17:57:01.819189-05:00",
                                      }
                                   ],
                              })
    
            