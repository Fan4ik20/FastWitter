from fastapi import Depends
from database.settings import BlogSession
from database.interfaces.user_interface import UserInterface
from database import models

from fastapi_jwt_auth import AuthJWT


def get_db() -> BlogSession:
    db = BlogSession()
    try:
        yield db
    finally:
        db.close()


class PaginationQueryParams:
    def __init__(self, offset: int = 0, limit: int = 100) -> None:
        self.offset = offset
        self.limit = limit


def authentication_needed(authorize: AuthJWT = Depends(AuthJWT)):
    authorize.jwt_required()


def get_active_user(
        logged_in=Depends(authentication_needed),
        authorize: AuthJWT = Depends(AuthJWT),
        db: BlogSession = Depends(get_db)
) -> models.User:
    active_username = authorize.get_jwt_subject()

    user = UserInterface.get_user_by_username(db, active_username)
    return user
