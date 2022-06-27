from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from fastapi_jwt_auth.exceptions import AuthJWTException

import uvicorn

import config

from routers import auth

from routers.users import users
from routers.users import user_followers

from routers.posts import user_posts
from routers.posts import posts

from routers.comments import comments
from routers.comments import post_comments
from routers.comments import user_comments

import exc

from database.interfaces.db_service import DbInterface


app = FastAPI(docs_url='/api/v1/docs/')
DbInterface.create_tables()

app.include_router(auth.router, prefix='/api/v1')
app.include_router(users.router, prefix='/api/v1')
app.include_router(user_followers.router, prefix='/api/v1')
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
                f'Requested {exc_.model} with given identifier not found',
            'place': 'path'
        }
    )


@app.exception_handler(exc.ObjectWithGivenAttrAlreadyExist)
def object_with_given_attr_exist_handler(
        request: Request, exc_: exc.ObjectWithGivenAttrAlreadyExist
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            'message':
                f'{exc_.model} with given {exc_.conflict_attr} already exist',
            'place': 'body'
        }
    )


@app.exception_handler(exc.NotObjectOwner)
def not_object_owner_handler(request: Request, exc_: exc.NotObjectOwner):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={'message': f'You are the not owner of this {exc_.model}'}
    )


@app.exception_handler(exc.CantPerformThis)
def cant_do_it_again_handler(request: Request, exc_: exc.CantPerformThis):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={'message': exc_.msg}
    )


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc_: AuthJWTException):
    return JSONResponse(
        status_code=exc_.status_code,
        content={'detail': exc_.message}
    )


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=65432)
