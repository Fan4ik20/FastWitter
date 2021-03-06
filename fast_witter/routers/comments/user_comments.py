from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from exceptions import exc

from schemas import comment_schemas as schemas

from database import models
from database.interfaces.comment_interface import CommentInterface
from database.interfaces.user_interface import UserInterface

from dependencies import BlogSession, PaginationQueryParams, get_active_user


router = APIRouter(prefix='/users/{user_id}/comments', tags=['User Comments'])


def raise_exc_if_user_not_exist(user_id: int, db: Session) -> None:
    user = UserInterface.get_user(db, user_id)

    if user is None:
        raise exc.RequestedObjectNotFound('User')


@router.get('/', response_model=list[schemas.Comment])
def get_user_comments(
        user_id: int, pagination_params: PaginationQueryParams = Depends(),
        db: Session = Depends(BlogSession)
):
    raise_exc_if_user_not_exist(user_id, db)

    return CommentInterface.get_users_comments(
        db, user_id, pagination_params.offset, pagination_params.limit
    )


@router.get('/{comment_id}/', response_model=schemas.CommentDetail)
def get_user_comment(
        user_id: int, comment_id: int, db: Session = Depends(BlogSession)
):
    raise_exc_if_user_not_exist(user_id, db)

    comment = CommentInterface.get_user_comment_with_related(
        db, user_id, comment_id
    )

    if comment is None:
        raise exc.RequestedObjectNotFound('Comment')

    return comment


@router.delete(
    '/{comment_id}/', response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user_comment(
        user_id: int, comment_id: int, db: Session = Depends(BlogSession),
        active_user: models.User = Depends(get_active_user)
):
    raise_exc_if_user_not_exist(user_id, db)

    if active_user.id != user_id:
        raise exc.NotObjectOwner('Comment')

    comment = CommentInterface.get_user_comment(db, user_id, comment_id)
    if comment is None:
        raise exc.RequestedObjectNotFound('Comment')

    CommentInterface.delete_comment(db, comment)
