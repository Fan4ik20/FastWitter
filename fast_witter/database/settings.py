from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from config import AppSettings


def create_db_engine(app_config: AppSettings) -> Engine:
    return create_engine(app_config.DB_URL)


def create_sessionmaker(engine: Engine) -> sessionmaker:
    return sessionmaker(autoflush=False, bind=engine)
