from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

import exc
import schemas
from database import models

from database.interfaces.comment_interface import CommentInterface
from dependencies import get_db, PaginationQueryParams, get_active_user


router = APIRouter(prefix='/users/{user_id}/comments', tags=['Comments'])


@router.get('/', response_model=list[schemas.Comment])
def get_users_comments(
        user_id: int, pagination_params: PaginationQueryParams = Depends(),
        db: Session = Depends(get_db)
):
    return CommentInterface.get_users_comments(
        db, user_id, pagination_params.offset, pagination_params.limit
    )


@router.get('/{comment_id}/', response_model=schemas.Comment)
def get_user_comment(
        user_id: int, comment_id: int, db: Session = Depends(get_db)
):

    comment = CommentInterface.get_user_comment(db, user_id, comment_id)

    if comment is None:
        raise exc.RequestedObjectNotFound('Comment')

    return comment


@router.delete(
    '/{comment_id}/', response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user_comment(
        user_id: int, comment_id: int, db: Session = Depends(get_db),
        active_user: models.User = Depends(get_active_user)
):
    if active_user.id != user_id:
        raise exc.NotObjectOwner('Comment')

    comment = CommentInterface.get_user_comment(db, user_id, comment_id)
    if comment is None:
        raise exc.RequestedObjectNotFound('Comment')

    CommentInterface.delete_comment(db, comment)
