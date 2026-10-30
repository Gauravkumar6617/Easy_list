from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from server.db.database import get_db
from server.models.users import User
from server.repositories.userRepositories import UserRepository
from server.utils.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v2/auth/login")


def get_current_user(
	token: Annotated[str, Depends(oauth2_scheme)],
	db: Annotated[Session, Depends(get_db)],
) -> User:
	unauthorized = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
		headers={"WWW-Authenticate": "Bearer"},
	)

	try:
		username = decode_access_token(token)
	except Exception:
		raise unauthorized from None

	if not username:
		raise unauthorized

	user = UserRepository(db).get_user_by_username(username)
	if user is None:
		raise unauthorized

	return user

