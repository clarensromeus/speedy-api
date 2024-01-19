from datetime import datetime
from annotated_types import Predicate, Len, Timezone
from typing import Annotated,TypedDict
# internally relative imports
from ...utils.user import email_check
from ...enums.index import MemberRole

class UserBase(TypedDict):
    username: Annotated[str, Len(min_length=5, max_length=25), Predicate(str.isalpha)]
    hashed_password: Annotated[str, Len(min_length=8, max_length=30)]
    email: Annotated[str, Predicate(str.isalnum), Predicate(email_check)]
    role: Annotated[str, Len(max_length=len(MemberRole.ADMINISTRATOR.value), 
                             min_length=len(MemberRole.GUEST.value)), Predicate(str.isalpha)]
    date_joined: Annotated[datetime, Timezone("America/Port-au-prince")]
    proffession: Annotated[str, Len(min_length=5, max_length=30), Predicate(str.isalpha), Predicate(str.upper)]