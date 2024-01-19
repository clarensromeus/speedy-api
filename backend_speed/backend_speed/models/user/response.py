from pydantic import BaseModel, Field, StrictStr, StrictBool
from typing import Optional

class Response(BaseModel):
    message: StrictStr
    success: StrictBool