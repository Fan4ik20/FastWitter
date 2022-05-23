from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.orm import Session

import schemas

from dependencies import get_db, PaginationQueryParams
from database.interfaces import PostInterface

router = APIRouter(prefix='/posts', tags=['posts'])


@router.get('/', response_model=list[schemas.Post])
def get_posts(
        pagination_params: PaginationQueryParams = Depends(),
        db: Session = Depends(get_db)
):
    return PostInterface.get_all_posts(
        db, pagination_params.offset, pagination_params.limit
    )


@router.get('/{post_id}/', response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = PostInterface.get_post(db, post_id)

    if post is None:
        raise HTTPException(404, detail='Post with given id does not exist')

    return post


@router.delete(
    '/{post_id}/', status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    if PostInterface.delete_post(db, post_id) is None:
        raise HTTPException(404, detail='Post with given id does not exist')
