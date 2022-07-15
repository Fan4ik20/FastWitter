from fastapi import status

import unittest

from tests.base import UserTestBase
from tests.factories import UserFactory

from database import models
from database.interfaces.user_interface import UserInterface

from schemas.user_schemas import User as UserSchema


class TestUserRoutes(UserTestBase):
    def setUp(self) -> None:
        super().setUp()

        self.users = [UserFactory() for _ in range(10)]
    
    def test_get_users(self) -> None:
        response = self.client.get(
            '/api/v1/users/', params={'limit': 5}
        )

        serialized_users = [
            self._serialize_user(user) for user in self.users[:5]
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for received_user in response.json():
            with self.subTest():
                self.assertIn(received_user, serialized_users)

    def test_create_user(self) -> None:
        payload = {
            'username': 'test_username',
            'email': 'test@test.com',
            'password': 'testPassword'
        }

        user_before = UserInterface.get_user_by_username(
            self.db, payload['username']
        )

        self.assertIsNone(user_before)

        response = self.client.post(
            '/api/v1/users/', json=payload
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = UserInterface.get_user_by_username(self.db, payload['username'])
        with self.subTest():
            self.assertEqual(user.username, payload['username'])
            self.assertEqual(user.email, payload['email'])

    def test_create_user_with_wrong_data(self) -> None:
        payload = {
            'user_name': 'test_username',
            'email': 'test_email'
        }

        response = self.client.post(
            '/api/v1/users/', json=payload
        )

        self.assertEqual(
            response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY
        )

        self.assertIsNone(
            UserInterface.get_user_by_username(self.db, payload['user_name'])
        )

    def test_get_user(self) -> None:
        for user in self.users:
            response = self.client.get(f'/api/v1/users/{user.id}')

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            content = response.json()
            self.assertEqual(content, self._serialize_user(user))

    def test_get_user_with_invalid_id(self) -> None:
        invalid_ids = [-1, len(self.users) + 5, 100]

        for id_ in invalid_ids:
            response = self.client.get(f'/api/v1/users/{id_}/')

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_current_user(self) -> None:
        user = self.users[0]

        token = self._generate_token(user.username)

        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.get(
            '/api/v1/users/me/', headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serialized_users = self._serialize_user(user, exclude_none=True)
        self.assertEqual(response.json(), serialized_users)

    def test_get_current_user_non_authorized(self) -> None:
        response = self.client.get('/api/v1/users/me/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


if __name__ == '__main__':
    unittest.main()
