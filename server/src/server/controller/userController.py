from fastapi import HTTPException, status
from server.schemas.userSchema import UserCreate
from server.services.userService import UserService
from server.models.users import User

class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def register_user(self, user_in: UserCreate) -> User:
        """
        Controller logic for signing up a user.
        """
        # 1. Check if the username already exists
        existing_user = self.user_service.get_user_by_username(user_in.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is already registered."
            )
            
        # 2. Hand off registration execution to the service layer
        return self.user_service.create_user(user_in)