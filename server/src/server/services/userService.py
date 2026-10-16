from server.models.users import User
from server.schemas.userSchema import UserCreate
from server.repositories.userRepositories import UserRepository
from server.utils.security import get_password_hash 

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_create: UserCreate) -> User:
    
  #model dump used to create dictonry and exclude password from it and then hash the password and add it to the dictionary
        user_data = user_create.model_dump(exclude={"password"})
#first hash the password and then add it to the dictionary
        user_data["hashed_password"] = get_password_hash(user_create.password)


        return self.user_repository.create_user(user_data)

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_repository.get_user_by_id(user_id)

    def get_user_by_username(self, username: str) -> User:
        return self.user_repository.get_user_by_username(username)