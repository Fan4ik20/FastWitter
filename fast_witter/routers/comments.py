from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

import schemas
import errors

from dependencies import get_db, PaginationQueryParams
from database.interfaces import CommentInterface

router = APIRouter(prefix='/comments', tags=['comments'])


@router.get('/', response_model=list[schemas.Comment])
def get_comments(
        pagination_params: PaginationQueryParams = Depends(),
        db: Session = Depends(get_db)
):
    return CommentInterface.get_all_comments(
        db, pagination_params.offset, pagination_params.limit
    )


@router.get('/{comment_id}/', response_model=schemas.CommentBase)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = CommentInterface.get_comment(db, comment_id)

    errors.raise_not_found_if_none(comment, 'Comment')

    return comment


@router.delete(
    '/{comment_id}/', response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = CommentInterface.get_comment(db, comment_id)

    errors.raise_not_found_if_none(comment, 'Comment')

    CommentInterface.delete_comment(db, comment)
