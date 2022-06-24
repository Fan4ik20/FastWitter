from fastapi import APIRouter, Depends, status
from fastapi import Response

from sqlalchemy.orm import Session

from schemas import post_schemas as schemas

import exc

from dependencies import get_db, PaginationQueryParams, get_active_user

from database import models
from database.interfaces.user_interface import UserInterface
from database.interfaces.post_interface import PostInterface

router = APIRouter(prefix='/users/{user_id}/posts', tags=['Posts'])


def get_user_post_or_raise_exc(
        user_id: int, post_id: int, db: Session
) -> models.Post:
    user = UserInterface.get_user(db, user_id)
    if user is None:
        raise exc.RequestedObjectNotFound('User')

    post = PostInterface.get_user_post(db, user_id, post_id)

    if post is None:
        raise exc.RequestedObjectNotFound('Post')

    return post


@router.get('/', response_model=list[schemas.Post])
def get_users_posts(
        user_id: int, pagination_params: PaginationQueryParams = Depends(),
        db: Session = Depends(get_db)
):
    user = UserInterface.get_user(db, user_id)
    if user is None:
        raise exc.RequestedObjectNotFound('User')

    return PostInterface.get_users_posts(
        db, user_id, pagination_params.offset, pagination_params.limit
    )


@router.get(
    '/{post_id}/', response_model=schemas.Post,
    status_code=status.HTTP_201_CREATED
)
def get_user_post(user_id: int, post_id: int, db: Session = Depends(get_db)):
    post = get_user_post_or_raise_exc(user_id, post_id, db)

    return post


@router.delete(
    '/{post_id}/', response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user_post(
        user_id: int, post_id: int, db: Session = Depends(get_db),
        active_user: models.User = Depends(get_active_user)
):
    if active_user.id != user_id:
        raise exc.NotObjectOwner('Post')

    post = get_user_post_or_raise_exc(user_id, post_id, db)

    PostInterface.delete_post(db, post)


@router.post('/{post_id}/like/', status_code=status.HTTP_201_CREATED)
def like_post(
        user_id: int, post_id: int, db: Session = Depends(get_db),
        active_user: models.User = Depends(get_active_user)
):
    post = get_user_post_or_raise_exc(user_id, post_id, db)

    PostInterface.like_post(db, post, active_user)

    return {'status': 'OK'}


@router.post('/{post_id}/unlike/', status_code=status.HTTP_201_CREATED)
def unlike_post(
        user_id: int, post_id: int, db: Session = Depends(get_db),
        active_user: models.User = Depends(get_active_user)
):
    post = get_user_post_or_raise_exc(user_id, post_id, db)

    PostInterface.unlike_post(db, post, active_user)

    return {'status': 'OK'}
