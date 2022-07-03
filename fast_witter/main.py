from fastapi import FastAPI
from fastapi_jwt_auth.exceptions import AuthJWTException

import uvicorn

import config

from exceptions import exc, handlers

from database.interfaces.db_service import DbInterface

from routers import blog_router


def include_routers(fastapi_app: FastAPI) -> None:
    fastapi_app.include_router(blog_router.router)


def include_handlers(fastapi_app: FastAPI) -> None:
    fastapi_app.add_exception_handler(
        exc.RequestedObjectNotFound, handlers.request_object_not_found_handler
    )
    fastapi_app.add_exception_handler(
        exc.ObjectWithGivenAttrAlreadyExist,
        handlers.object_with_given_attr_exist_handler
    )
    fastapi_app.add_exception_handler(
        exc.NotObjectOwner, handlers.not_object_owner_handler
    )
    fastapi_app.add_exception_handler(
        exc.CantPerformThis, handlers.cant_perform_this_handler
    )
    fastapi_app.add_exception_handler(
        AuthJWTException, handlers.authjwt_exception_handler
    )


def create_app() -> FastAPI:
    fastapi_app = FastAPI(docs_url='/api/v1/docs/')
    DbInterface.create_tables()

    include_routers(fastapi_app)
    include_handlers(fastapi_app)

    return fastapi_app


app = create_app()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=65432)
