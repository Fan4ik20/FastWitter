import os

from pydantic import BaseModel

from dotenv import load_dotenv

from fastapi_jwt_auth import AuthJWT

load_dotenv('.env')

SECRET_KEY = os.getenv('SECRET_KEY')


class Settings(BaseModel):
    authjwt_secret_key: str


@AuthJWT.load_config
def get_config():
    return Settings(authjwt_secret_key=SECRET_KEY)
