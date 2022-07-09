from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from schemas import user_schemas as schemas

from exceptions import exc

from database.interfaces.user_interface import UserInterface
from database.models import User

from dependencies import BlogSession, PaginationQueryParams, get_active_user

router = APIRouter(
    prefix='/users/{user_id}', tags=['User Followers|Following']
)


def get_user_or_raise_exc(user_id: int, db: Session) -> User:
    user = UserInterface.get_user(db, user_id)

    if user is None:
        raise exc.RequestedObjectNotFound('User')

    return user


@router.get('/followers/', response_model=list[schemas.User])
def get_user_followers(
        user_id: int, db: Session = Depends(BlogSession),
        pagination_params: PaginationQueryParams = Depends()
):
    get_user_or_raise_exc(user_id, db)

    user_followers = UserInterface.get_user_followers(
        db, user_id, pagination_params.offset, pagination_params.limit
    )

    return user_followers


@router.get('/following/', response_model=list[schemas.User])
def get_user_following(
        user_id: int, db: Session = Depends(BlogSession),
        pagination_params: PaginationQueryParams = Depends()
):
    get_user_or_raise_exc(user_id, db)

    following = UserInterface.get_user_following(
        db, user_id, pagination_params.offset, pagination_params.limit
    )

    return following


@router.post('/follow/')
def follow_user(
        user_id: int, db: Session = Depends(BlogSession),
        active_user: User = Depends(get_active_user)
):
    followed = get_user_or_raise_exc(user_id, db)

    if user_id == active_user.id:
        raise exc.CantPerformThis('You can\'t follow yourself')

    if UserInterface.is_user_followed(db, user_id, active_user.id):
        raise exc.CantPerformThis('You can\'t follow again')

    UserInterface.follow_user(db, followed, active_user)

    return {'status': 'OK'}


@router.post('/unfollow/')
def unfollow_user(
        user_id: int, db: Session = Depends(BlogSession),
        active_user: User = Depends(get_active_user)
):
    followed = get_user_or_raise_exc(user_id, db)

    if user_id == active_user.id:
        raise exc.CantPerformThis('You can\'t unfollow yourself')

    if not UserInterface.is_user_followed(db, user_id, active_user.id):
        raise exc.CantPerformThis('You can\'t unfollow without being followed')

    UserInterface.unfollow_user(db, followed, active_user)

    return {'status': 'OK'}
