import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import models


test_engine = create_engine(os.getenv('DB_URL_TEST'))

TestSession = sessionmaker(bind=test_engine)


def create_test_tables() -> None:
    models.BlogBase.metadata.create_all(bind=test_engine)


def drop_test_tables() -> None:
    models.BlogBase.metadata.drop_all(bind=test_engine)


def get_test_db() -> TestSession:
    db = TestSession()

    try:
        yield db
    finally:
        db.close()
