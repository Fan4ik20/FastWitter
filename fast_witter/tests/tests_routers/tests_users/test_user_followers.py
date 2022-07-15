import unittest
from typing import Iterable, Literal

from fastapi import status

from database import models
from tests.factories import UserFactory
from tests.base import UserTestBase

from database.interfaces.user_interface import UserInterface


class TestUserFollowersRoutes(UserTestBase):
    def setUp(self) -> None:
        super().setUp()

        self.following = [UserFactory() for _ in range(5)]
        self.user = UserFactory.create(following=self.following, username='X')
        self.followers = [
            UserFactory.create(following=(self.user,)) for _ in range(7)
        ]

        self.followers_url = f'/api/v1/users/{self.user.id}/followers/'
        self.following_url = f'/api/v1/users/{self.user.id}/following/'

    def test_get_user_followers(self) -> None:
        offset, limit = 1, 5
        serialized_users = [
            self._serialize_user(user)
            for user in self.followers[offset: offset + limit]
        ]

        response = self.client.get(
            self.followers_url, params={'offset': offset, 'limit': limit}
        )
        received_content = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(received_content), limit)

        for received_user in received_content:
            self.assertIn(received_user, serialized_users)

    def test_get_user_followers_with_wrong_user_id(self) -> None:
        user_id = 5521

        response = self.client.get(f'/api/v1/users/{user_id}/followers/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_following(self) -> None:
        serialized_users = [
            self._serialize_user(user)
            for user in self.following
        ]

        response = self.client.get(self.following_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for user in response.json():
            self.assertIn(user, serialized_users)

    def _refresh_users(self, users: Iterable[models.User]) -> None:
        for user in users:
            self.db.refresh(user)

    def test_follow_user(self) -> None:
        headers = self._get_auth_headers(self.user.username)

        for test_user in self.followers:
            old_following_count = self.user.following_count
            old_followers_count = test_user.followers_count

            response = self.client.post(
                f'/api/v1/users/{test_user.id}/follow/', headers=headers
            )
            followers = UserInterface.get_user_followers(self.db, test_user.id)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn(self.user, followers)

            self._refresh_users((self.user, test_user))

            new_following_count = self.user.following_count
            new_followers_count = test_user.followers_count

            with self.subTest():
                self.assertEqual(new_followers_count, old_followers_count + 1)
                self.assertEqual(new_following_count, old_following_count + 1)

    def _test_follow_unfollow_yourself(
            self, action: Literal['follow'] | Literal['unfollow']
    ) -> None:
        headers = self._get_auth_headers(self.user.username)
        self._refresh_users((self.user,))

        followers_count = self.user.followers_count
        following_count = self.user.following_count

        response = self.client.post(
            f'/api/v1/users/{self.user.id}/{action}/', headers=headers
        )

        self._refresh_users((self.user,))

        new_followers_count = self.user.followers_count
        new_following_count = self.user.following_count

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        self.assertEqual(following_count, new_following_count)
        self.assertEqual(followers_count, new_followers_count)

    def test_follow_yourself(self) -> None:
        self._test_follow_unfollow_yourself('follow')

    def _test_follow_unfollow_again(
            self, action: Literal['follow'] | Literal['unfollow']
    ) -> None:
        headers = self._get_auth_headers(self.user.username)

        users = self.following if action == 'follow' else self.followers

        for followed in users:
            followers_count = followed.followers_count
            following_count = self.user.following_count

            response = self.client.post(
                f'/api/v1/users/{followed.id}/{action}/', headers=headers
            )

            self._refresh_users((self.user, followed))

            new_followers_count = followed.followers_count
            new_following_count = self.user.following_count

            self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

            with self.subTest():
                self.assertEqual(following_count, new_following_count)
                self.assertEqual(followers_count, new_followers_count)

    def test_follow_user_again(self) -> None:
        self._test_follow_unfollow_again('follow')

    def test_follow_user_unauthorized(self) -> None:
        response = self.client.post(f'/api/v1/users/{self.user.id}/follow/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unfollow_user(self) -> None:
        headers = self._get_auth_headers(self.user.username)

        for followed in self.following:
            followers_count = followed.followers_count
            following_count = self.user.following_count

            response = self.client.post(
                f'/api/v1/users/{followed.id}/unfollow/', headers=headers
            )

            self._refresh_users((self.user, followed))

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            new_followers_count = followed.followers_count
            new_following_count = self.user.following_count

            with self.subTest():
                self.assertEqual(following_count - 1, new_following_count)
                self.assertEqual(followers_count - 1, new_followers_count)

    def test_unfollow_yourself(self) -> None:
        self._test_follow_unfollow_yourself('unfollow')

    def test_unfollow_again(self) -> None:
        self._test_follow_unfollow_again('unfollow')


if __name__ == '__main__':
    unittest.main()
