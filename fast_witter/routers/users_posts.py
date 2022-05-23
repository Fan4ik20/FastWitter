from fastapi import APIRouter, HTTPException, Depends, status

from sqlalchemy.orm import Session

import schemas
from dependencies import get_db, PaginationQueryParams
from database.interfaces import PostInterface

router = APIRouter(prefix='/users/{user_id}/posts', tags=['users_posts'])


@router.get('/', response_model=list[schemas.Post])
def get_users_posts(
        user_id: int, pagination_params: PaginationQueryParams = Depends(),
        db: Session = Depends(get_db)
):
    return PostInterface.get_users_posts(
        db, user_id, pagination_params.offset, pagination_params.limit
    )


@router.post('/', response_model=schemas.Post)
def create_post(
        user_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)
):
    # TODO. Check if user exists

    return PostInterface.create_post(db, post, user_id)


@router.get(
    '/{post_id}/', response_model=schemas.Post,
    status_code=status.HTTP_201_CREATED
)
def get_user_post(user_id: int, post_id: int, db: Session = Depends(get_db)):
    post = PostInterface.get_user_post(db, user_id, post_id)

    if post is None:
        raise HTTPException(
            404, detail='Post with given post_id and user_id does not exist'
        )

    return post
