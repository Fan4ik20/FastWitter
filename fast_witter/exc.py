class RequestedObjectNotFound(Exception):
    def __init__(self, model: str) -> None:
        self.model = model


class ObjectWithGivenAttrAlreadyExist(Exception):
    def __init__(self, model: str, conflict_attr: str):
        self.model = model
        self.conflict_attr = conflict_attr
