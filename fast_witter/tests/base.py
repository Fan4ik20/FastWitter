from unittest import TestCase

from fastapi.testclient import TestClient
from fastapi_jwt_auth import AuthJWT

from main import app
from dependencies import BlogSession

from tests.service import (
    get_test_db, create_test_tables, drop_test_tables, test_session
)


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
