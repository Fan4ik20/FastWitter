from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from exceptions import exc

from schemas import comment_schemas as schemas

from dependencies import BlogSession, PaginationQueryParams
from database.interfaces.comment_interface import CommentInterface

router = APIRouter(prefix='/comments', tags=['Comments'])


@router.get('/', response_model=list[schemas.Comment])
def get_comments(
        pagination_params: PaginationQueryParams = Depends(),
        db: Session = Depends(BlogSession)
):
    return CommentInterface.get_all_comments(
        db, pagination_params.offset, pagination_params.limit
    )


@router.get('/{comment_id}/', response_model=schemas.CommentDetail)
def get_comment(comment_id: int, db: Session = Depends(BlogSession)):
    comment = CommentInterface.get_comment_with_related(db, comment_id)

    if comment is None:
        raise exc.RequestedObjectNotFound('Comment')

    return comment
