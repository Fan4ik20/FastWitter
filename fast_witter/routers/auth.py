from fastapi import APIRouter, Depends

from fastapi_jwt_auth import AuthJWT

from sqlalchemy.orm import Session

from security import service

from database.interfaces.user_interface import UserInterface

from dependencies import BlogSession
from schemas import user_schemas

from exceptions import exc

router = APIRouter(tags=['Authentication'])


@router.post('/login/')
def login(
        user: user_schemas.UserLogin,
        authorize: AuthJWT = Depends(), db: Session = Depends(BlogSession)
):
    db_user = UserInterface.get_user_by_username(
        db, user.username
    )

    if db_user is None:
        raise exc.CredentialsException
    if not service.verify_password(user.password, db_user.hashed_password):
        raise exc.CredentialsException

    access_token = authorize.create_access_token(subject=user.username)

    return {'access_token': access_token}
