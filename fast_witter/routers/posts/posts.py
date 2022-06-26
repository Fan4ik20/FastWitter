from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

import exc

from schemas import post_schemas as schemas

from database import models
from database.interfaces.post_interface import PostInterface

from dependencies import get_db, PaginationQueryParams, get_active_user


router = APIRouter(prefix='/posts', tags=['Posts'])


@router.get('/', response_model=list[schemas.Post])
def get_posts(
        pagination_params: PaginationQueryParams = Depends(),
        db: Session = Depends(get_db)
):
    return PostInterface.get_all_posts(
        db, pagination_params.offset, pagination_params.limit
    )


@router.post(
    '/', response_model=schemas.Post, status_code=status.HTTP_201_CREATED
)
def create_post(
        post: schemas.PostCreate, db: Session = Depends(get_db),
        active_user: models.User = Depends(get_active_user)
):
    post = PostInterface.create_post(db, post, active_user.id)

    return post


@router.get('/{post_id}/', response_model=schemas.PostDetail)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = PostInterface.get_post_with_related(db, post_id)

    if post is None:
        raise exc.RequestedObjectNotFound('Post')

    return post
