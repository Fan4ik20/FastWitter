from fastapi import APIRouter, Depends

from fastapi_jwt_auth import AuthJWT

from sqlalchemy.orm import Session

import schemas

from security import service

from database.interfaces.user_interface import UserInterface

from dependencies import get_db

import exc


router = APIRouter(tags=['Authentication'])


@router.post('/login/')
def login(
        user: schemas.UserLogin,
        authorize: AuthJWT = Depends(), db: Session = Depends(get_db)
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
