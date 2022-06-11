from fastapi import APIRouter, Depends, status
from fastapi import Response

from sqlalchemy.orm import Session

import schemas

import exc

from dependencies import get_db, PaginationQueryParams
from database.interfaces import PostInterface, UserInterface

router = APIRouter(prefix='/users/{user_id}/posts', tags=['Posts'])


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


@router.post('/', response_model=schemas.Post)
def create_post(
        user_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)
):
    user = UserInterface.get_user(db, user_id)

    if user is None:
        raise exc.RequestedObjectNotFound('User')

    return PostInterface.create_post(db, post, user_id)


@router.get(
    '/{post_id}/', response_model=schemas.Post,
    status_code=status.HTTP_201_CREATED
)
def get_user_post(user_id: int, post_id: int, db: Session = Depends(get_db)):
    user = UserInterface.get_user(db, user_id)
    if user is None:
        raise exc.RequestedObjectNotFound('User')

    post = PostInterface.get_user_post(db, user_id, post_id)

    if post is None:
        raise exc.RequestedObjectNotFound('Post')

    return post


@router.delete(
    '/{post_id}/', response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user_post(
        user_id: int, post_id: int, db: Session = Depends(get_db)
):
    user = UserInterface.get_user(db, user_id)
    if user is None:
        raise exc.RequestedObjectNotFound('User')

    post = PostInterface.get_post(db, post_id)
    if post is None:
        raise exc.RequestedObjectNotFound('Post')

    PostInterface.delete_post(db, post)
