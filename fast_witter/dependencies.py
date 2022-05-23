from database.settings import BlogSession


def get_db() -> BlogSession:
    db = BlogSession()
    try:
        yield db
    finally:
        db.close()


class PaginationQueryParams:
    def __init__(self, offset: int = 0, limit: int = 100) -> None:
        self.offset = offset
        self.limit = limit
