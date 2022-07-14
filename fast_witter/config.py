from pydantic import BaseModel, BaseSettings, Field

from fastapi_jwt_auth import AuthJWT


class AppSettings(BaseSettings):
    DB_URL: str
    SECRET_KEY: str


class TestSettings(AppSettings):
    DB_URL: str = Field('sqlite:///./test.db', env='DB_URL_TEST')


class Settings(BaseModel):
    authjwt_secret_key: str


@AuthJWT.load_config
def get_config():
    # FIXME.
    return Settings(
        authjwt_secret_key=AppSettings(_env_file='.env').SECRET_KEY
    )
