from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

import errors
from security import service as security

from database.interfaces import UserInterface
from dependencies import get_db

router = APIRouter(prefix='/', tags=['authentication'])


@router.post('/token/')
def get_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = UserInterface.get_user_by_username(db, form_data.username)

    errors.raise_not_found_if_none(user, 'User')
    errors.authenticate_or_raise_unauthorized(
        form_data.password, user.hashed_password
    )
