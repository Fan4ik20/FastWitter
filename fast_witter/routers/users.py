from fastapi import APIRouter, Depends, status

from fastapi_jwt_auth import AuthJWT

from sqlalchemy.orm import Session

import schemas
import exc

from dependencies import get_db, PaginationQueryParams
from database.interfaces.user_interface import UserInterface

router = APIRouter(
    prefix='/users', tags=['Users']
)


@router.get('/', response_model=list[schemas.User])
def get_users(
        pagination_params: PaginationQueryParams = Depends(),
        db: Session = Depends(get_db)
):
    """Retrieves a list of all users"""

    return UserInterface.get_all_users(
        db, pagination_params.offset, pagination_params.limit
    )


@router.post(
    '/', response_model=schemas.User, status_code=status.HTTP_201_CREATED
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if UserInterface.get_user_by_email(db, user.email):
        raise exc.ObjectWithGivenAttrAlreadyExist('User',  'Email')
    if UserInterface.get_user_by_username(db, user.username):
        raise exc.ObjectWithGivenAttrAlreadyExist('User', 'Username')

    return UserInterface.create_user(db, user)


@router.get('/me/', response_model=schemas.User)
def get_current_user(
        authorize: AuthJWT = Depends(), db: Session = Depends(get_db)
):
    authorize.jwt_required()

    current_username = authorize.get_jwt_subject()

    user = UserInterface.get_user_by_username(db, current_username)

    return user


@router.get('/{user_id}/', response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = UserInterface.get_user(db, user_id)

    if user is None:
        raise exc.RequestedObjectNotFound('User')

    return user
