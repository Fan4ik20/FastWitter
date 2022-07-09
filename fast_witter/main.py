from fastapi import FastAPI
from fastapi_jwt_auth.exceptions import AuthJWTException

import uvicorn

from config import AppSettings

from exceptions import exc, handlers

from database.settings import create_db_engine, create_sessionmaker
from database.interfaces.db_service import DbInterface

from dependencies import BlogSession, get_db_session

from routers import blog_router


def include_routers(fastapi_app: FastAPI) -> None:
    fastapi_app.include_router(blog_router.router, prefix='/api/v1')


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


def include_db(app_: FastAPI, config: AppSettings):
    blog_engine = create_db_engine(config)
    blog_sessionmaker = create_sessionmaker(blog_engine)

    DbInterface.create_tables(blog_engine)

    app_.dependency_overrides[BlogSession] = get_db_session(blog_sessionmaker)


def create_app() -> FastAPI:
    fastapi_app = FastAPI(docs_url='/api/v1/docs/')
    app_config = AppSettings(_env_file='.env')

    include_db(fastapi_app, app_config)

    include_routers(fastapi_app)
    include_handlers(fastapi_app)

    return fastapi_app


app = create_app()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=65432)
