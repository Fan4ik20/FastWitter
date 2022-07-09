from fastapi import Depends

from sqlalchemy.orm import sessionmaker, Session

from database.interfaces.user_interface import UserInterface
from database import models

from fastapi_jwt_auth import AuthJWT


class BlogSession:
    pass


def get_db_session(sessionmaker_: sessionmaker):
    def get_db():
        with sessionmaker_() as db:
            yield db

    return get_db


class PaginationQueryParams:
    def __init__(self, offset: int = 0, limit: int = 100) -> None:
        self.offset = offset
        self.limit = limit


def authentication_needed(authorize: AuthJWT = Depends(AuthJWT)):
    authorize.jwt_required()


def get_active_user(
        logged_in=Depends(authentication_needed),
        authorize: AuthJWT = Depends(AuthJWT),
        db: Session = Depends(BlogSession)
) -> models.User:
    active_username = authorize.get_jwt_subject()

    user = UserInterface.get_user_by_username(db, active_username)
    return user
