from database.settings import BlogSession


def get_db() -> BlogSession:
    db = BlogSession()
    try:
        yield db
    finally:
        db.close()
