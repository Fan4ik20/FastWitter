from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import uvicorn

import config

from routers import users

from routers.posts import user_posts
from routers.posts import posts

from routers.comments import comments
from routers.comments import post_comments
from routers.comments import user_comments

import exc

from database.interfaces import DbInterface


app = FastAPI(docs_url='/api/v1/docs/')
DbInterface.create_tables()

app.include_router(users.router, prefix='/api/v1')
app.include_router(posts.router, prefix='/api/v1')
app.include_router(user_posts.router, prefix='/api/v1')
app.include_router(comments.router, prefix='/api/v1')
app.include_router(user_comments.router, prefix='/api/v1')
app.include_router(post_comments.router, prefix='/api/v1')


@app.exception_handler(exc.RequestedObjectNotFound)
def request_object_not_found_handler(
        request: Request, exc_: exc.RequestedObjectNotFound
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            'message':
                f'Requested {exc_.model} with given identifier not found'
        }
    )


@app.exception_handler(exc.ObjectWithGivenAttrAlreadyExist)
def user_already_registered_handler(
        request: Request, exc_: exc.ObjectWithGivenAttrAlreadyExist
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            'message':
                f'{exc_.model} with given {exc_.conflict_attr} already exist'
        }
    )


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=65432)
