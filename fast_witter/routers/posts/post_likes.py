from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from exceptions import exc

from dependencies import get_db, PaginationQueryParams, get_active_user

from database import models
from database.interfaces.user_interface import UserInterface
from database.interfaces.post_interface import PostInterface

from schemas import user_schemas


router = APIRouter(
    prefix='/users/{user_id}/posts/{post_id}', tags=['Post Likes']
)


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


@router.get('/likes/', response_model=list[user_schemas.User])
def get_liked_post_users(
        user_id, post_id, db: Session = Depends(get_db),
        pagination_params: PaginationQueryParams = Depends()
):
    get_user_post_or_raise_exc(user_id, post_id, db)

    liked_users = PostInterface.get_liked_post_users(
        db, post_id, pagination_params.offset, pagination_params.limit
    )

    return liked_users


@router.post('/like/')
def like_post(
        user_id: int, post_id: int, db: Session = Depends(get_db),
        active_user: models.User = Depends(get_active_user)
):
    post = get_user_post_or_raise_exc(user_id, post_id, db)

    if PostInterface.is_user_liked_post(db, active_user.id, post_id):
        raise exc.CantPerformThis('You can\'t like this post again')

    PostInterface.like_post(db, post, active_user)

    return {'status': 'OK'}


@router.post('/unlike/')
def unlike_post(
        user_id: int, post_id: int, db: Session = Depends(get_db),
        active_user: models.User = Depends(get_active_user)
):
    post = get_user_post_or_raise_exc(user_id, post_id, db)

    if not PostInterface.is_user_liked_post(db, active_user.id, post_id):
        raise exc.CantPerformThis('You can\'t unlike post without liking it')

    PostInterface.unlike_post(db, post, active_user)

    return {'status': 'OK'}
