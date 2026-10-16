from fastapi import Depends ,HTTPException ,APIRouter
from server.controller.userController import UserController
from server.schemas.userSchema import UserCreate
from server.services.userService import UserService
from server.repositories.userRepositories import UserRepository
from server.db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users")

def get_user_controller(db: Session = Depends(get_db)) -> UserController:
    repository = UserRepository(db)
    service = UserService(repository)
    return UserController(service)


@router.post("/register")
def register_user(user_in: UserCreate, user_controller: UserController = Depends(get_user_controller)):
    """
    Endpoint for user registration.
    """
    try:
        return user_controller.register_user(user_in)
    except HTTPException as e:
        raise e