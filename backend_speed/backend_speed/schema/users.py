# internally relative imports of resources
from ..Interface.user.user_interface import UserInterface

def userEmptity(user_data: UserInterface) -> UserInterface:
    return {
        "_id": str(user_data["_id"]),
        "hashed_password": user_data["hashed_password"],
        "role": ("GUEST", user_data["role"]) [user_data["role"] is None],
        "username": user_data["username"],
        "proffession": user_data["proffession"],
        "email": user_data["email"],
        "date_joined": user_data["date_joined"],
        "pictured_url": user_data["pictured_url"],
        "products": user_data["products"]
    }
    
def usersEmptity(users_data) -> list[UserInterface]:
    return [userEmptity(user) for user in users_data]