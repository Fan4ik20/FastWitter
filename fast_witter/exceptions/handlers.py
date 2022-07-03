from fastapi import Request, status
from fastapi.responses import JSONResponse

from fastapi_jwt_auth.exceptions import AuthJWTException

from exceptions import exc


def request_object_not_found_handler(
        _: Request, exc_: exc.RequestedObjectNotFound
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            'message':
                f'Requested {exc_.model} with given identifier not found',
            'place': 'path'
        }
    )


def object_with_given_attr_exist_handler(
        _: Request, exc_: exc.ObjectWithGivenAttrAlreadyExist
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            'message':
                f'{exc_.model} with given {exc_.conflict_attr} already exist',
            'place': 'body'
        }
    )


def not_object_owner_handler(_: Request, exc_: exc.NotObjectOwner):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={'message': f'You are the not owner of this {exc_.model}'}
    )


def cant_perform_this_handler(_: Request, exc_: exc.CantPerformThis):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={'message': exc_.msg}
    )


def authjwt_exception_handler(_: Request, exc_: AuthJWTException):
    return JSONResponse(
        status_code=exc_.status_code,
        content={'detail': exc_.message}
    )
