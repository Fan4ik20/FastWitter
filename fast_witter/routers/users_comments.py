from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import exc
import schemas

from database.interfaces import CommentInterface
from dependencies import get_db, PaginationQueryParams


router = APIRouter(prefix='/users/{user_id}/comments', tags=['users_comments'])


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
