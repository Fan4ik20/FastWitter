from unittest import TestCase

from fastapi.testclient import TestClient
from fastapi_jwt_auth import AuthJWT

from main import app
from dependencies import BlogSession

from tests.service import (
    get_test_db, create_test_tables, drop_test_tables, test_session
)

from database import models

from schemas.post_schemas import Post as PostSchema, PostDetail


app.dependency_overrides[BlogSession] = get_test_db


class TestBase(TestCase):
    def setUp(self) -> None:
        create_test_tables()

        self.client = TestClient(app)
        self.db = test_session()

    def tearDown(self) -> None:
        self.db.close()

        drop_test_tables()

    @staticmethod
    def _generate_token(username: str) -> str:
        authorize = AuthJWT()
        return authorize.create_access_token(subject=username)


class PostTestBase(TestBase):
    @staticmethod
    def _serialize_post(post: models.Post) -> dict:
        post_schema = PostSchema.from_orm(post)

        return post_schema.dict()

    @staticmethod
    def _serialize_detailed_post(post: models.Post) -> dict:
        post_schema = PostDetail.from_orm(post)

        return post_schema.dict(by_alias=True)
