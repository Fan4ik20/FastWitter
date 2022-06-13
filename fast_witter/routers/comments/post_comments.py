from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

import exc
import schemas
from database import models

from database.interfaces.comment_interface import CommentInterface
from database.interfaces.user_interface import UserInterface
from database.interfaces.post_interface import PostInterface

from dependencies import get_db, PaginationQueryParams, get_active_user

router = APIRouter(
    prefix='/users/{user_id}/posts/{post_id}/comments',
    tags=['Comments']
)


def raise_exc_if_user_post_not_exist(
        user_id: int, post_id: int, db: Session
) -> None:
    user = UserInterface.get_user(db, user_id)
    if user is None:
        raise exc.RequestedObjectNotFound('User')

    post = PostInterface.get_user_post(db, user_id, post_id)
    if post is None:
        raise exc.RequestedObjectNotFound('Post')


@router.get('/', response_model=list[schemas.Comment])
def get_post_comments(
        user_id: int, post_id: int,
        pagination_params: PaginationQueryParams = Depends(),
        db: Session = Depends(get_db)
):
    raise_exc_if_user_post_not_exist(user_id, post_id, db)

    comments = CommentInterface.get_user_post_comments(
        db, user_id, post_id, pagination_params.offset, pagination_params.limit
    )

    return comments


@router.post(
    '/', response_model=schemas.Comment,
    status_code=status.HTTP_201_CREATED
)
def create_post_comment(
        user_id: int, post_id: int, comment: schemas.CommentCreate,
        db: Session = Depends(),
        active_user: models.User = Depends(get_active_user)
):
    raise_exc_if_user_post_not_exist(user_id, post_id, db)

    comment = CommentInterface.create_comment(
        db, active_user.id, post_id, comment
    )

    return comment


def get_ind_comment_or_raise_exc(
        user_id: int, post_id: int, comment_id: int,
        db: Session = Depends(get_db)
):
    raise_exc_if_user_post_not_exist(user_id, post_id, db)

    comment = CommentInterface.get_user_post_comment(
        db, user_id, post_id, comment_id
    )

    if comment is None:
        raise exc.RequestedObjectNotFound('Comment')

    return comment


@router.get('/{comment_id}/', response_model=schemas.Comment)
def get_post_comment(
    user_id: int, post_id: int, comment_id: int, db: Session = Depends(get_db)
):
    comment = get_ind_comment_or_raise_exc(user_id, post_id, comment_id, db)

    return comment


@router.delete(
    '/{comment_id}/', response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_post_comment(
        user_id: int, post_id: int, comment_id: int,
        db: Session = Depends(get_db),
        active_user: models.User = Depends(get_active_user)
):
    comment = get_ind_comment_or_raise_exc(user_id, post_id, comment_id, db)

    if active_user.id != comment.user_id or active_user.id != user_id:
        raise exc.NotObjectOwner('Comment')

    CommentInterface.delete_comment(db, comment)
