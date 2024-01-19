from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, StrictInt, StrictBool
from typing import Annotated
from functools import lru_cache

class Setttings(BaseSettings):
    
    model_config = SettingsConfigDict(env_file="../../.env", env_file_encoding="utf8", 
                                      extra="ignore", populate_by_name=True, validate_default=True,
                                      env_prefix="SPEEDY_",
                                       json_schema_extra={
                                          "PROJECT_PORT": 5000,
                                          "PROJECT_DEBUG": "True",                                  
                                          "PROJECT_RELOADING": "True",
                                          "DATABASE_NAME": "E-COMMERCE",
                                          "DATABASE_PORT": 27017,
                                          "DATABASE_HOST": '127.0.0.1',
                                          "DATABASE_DRIVER_NAME": "mongodb"
                                        },
                                       validation_error_cause=True
                                      )
    
    PROJECT_PORT: StrictInt = 5000
    PROJECT_DEBUG: StrictBool = True
    PROJECT_RELOADING: StrictBool = Field(...)
    DATABASE_NAME: Annotated[str, Field(default="database_name", min_length=5, max_length=30, strict=True, 
                                        description="DATABASE_NAME")]
    DATABASE_PORT: Annotated[int, Field(default=27017, gt=2000, lt=100000, description="DATABASE_PORT", strict=True)]
    DATABASE_HOST: str = Field(...)
    DATABASE_DRIVER_NAME: Annotated[str, Field(default="mongodb", min_length=5, max_length=10, strict=True, 
                                               description="DATABASE_DRIVER_NAME")]

    

# function defined to retrieve data settings with the caching behavior for better file performance loading
@lru_cache
def GET_SETTINGS():
    SETTING_DATA = Setttings(DATABASE_HOST="127.0.0.1", 
                             PROJECT_RELOADING=True,
                             DATABASE_PORT=2717).model_dump(warnings=True)
    return SETTING_DATA
    




    
