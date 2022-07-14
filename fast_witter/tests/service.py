from sqlalchemy.orm import scoped_session, Session

from database import models
from database.settings import create_db_engine, create_sessionmaker

from config import TestSettings

app_config = TestSettings(_env_file='.env')

test_engine = create_db_engine(app_config)
TestSessionmaker = create_sessionmaker(test_engine)

test_session = scoped_session(TestSessionmaker)


def create_test_tables() -> None:
    models.BlogBase.metadata.create_all(bind=test_engine)


def drop_test_tables() -> None:
    models.BlogBase.metadata.drop_all(bind=test_engine)


def get_test_db() -> Session:
    db = TestSessionmaker()

    try:
        yield db
    finally:
        db.close()
