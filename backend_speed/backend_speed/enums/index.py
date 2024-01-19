from enum import Enum, verify, UNIQUE

@verify(UNIQUE)
class Proffession(str, Enum):
    FIRST_CLASS = "COMPUTER SICIENCE"
    SECOND_CLASS = "BUSINESSMAN"
    THIRD_CLASS = "CONTENT WRITER"
    FOURTH_CLASS = "ONLINE PRODUCER"

@verify(UNIQUE)    
class UserTags(str, Enum):
    SINGLE_USER = "SINGLE_USER",
    ALL_USER = "ALL_USER"

@verify(UNIQUE)
class SaleTags(str, Enum):
    SINGLE_SALE = "SINGLE_SALE"
    RELATED_SALES = "RELATED_SALES"
    ALL_SALES = "ALL_SALES"
 
@verify(UNIQUE)   
class ProductTags(str, Enum):
    SINGLE_PRODUCT = "SINGLE_PRODUCT"
    RELATED_PRODUCTS = "RELATED_PRODUCTS"
    ALL_PRODUCTS = "ALL_PRODUCTS"

@verify(UNIQUE)    
class MemberRole(str, Enum):
    ADMINISTRATOR = "ADMINISTRATOR"
    SECRETARY = "SECRETARY"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"
    GUEST = "GUEST"