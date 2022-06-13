from fastapi import HTTPException, status


class RequestedObjectNotFound(Exception):
    def __init__(self, model: str) -> None:
        self.model = model


class ObjectWithGivenAttrAlreadyExist(Exception):
    def __init__(self, model: str, conflict_attr: str):
        self.model = model
        self.conflict_attr = conflict_attr


class NotObjectOwner(Exception):
    def __init__(self, model: str):
        self.model = model


CredentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
