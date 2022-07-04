from unittest import TestCase

from fastapi.testclient import TestClient

from main import app
from dependencies import get_db

from tests.service import get_test_db, create_test_tables, drop_test_tables


app.dependency_overrides[get_db] = get_test_db


class TestBase(TestCase):
    def setUp(self) -> None:
        create_test_tables()

        self.client = TestClient(app)

    def tearDown(self) -> None:
        drop_test_tables()
