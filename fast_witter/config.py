from pydantic import BaseModel, BaseSettings, Field

from fastapi_jwt_auth import AuthJWT


class AppSettings(BaseSettings):
    DB_URL: str
    SECRET_KEY: str
    DB_URL_TEST: str | None = Field(None)


class Settings(BaseModel):
    authjwt_secret_key: str


@AuthJWT.load_config
def get_config():
    # FIXME.
    return Settings(
        authjwt_secret_key=AppSettings(_env_file='.env').SECRET_KEY
    )
