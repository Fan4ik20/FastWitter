import unittest
from typing import Iterable, Literal, TypeAlias

from fastapi import status

from database import models
from tests.base import UserTestBase
from tests.factories import PostFactory, UserFactory

from database.interfaces.post_interface import PostInterface


url: TypeAlias = str
like_unlike: TypeAlias = Literal['like'] | Literal['unlike']


class TestPostLikesRoutes(UserTestBase):
    def setUp(self) -> None:
        super().setUp()

        self.liked_users = [UserFactory() for _ in range(10)]
        self.owner = UserFactory(username='TEST')
        self.post = PostFactory.create(likes=self.liked_users, user=self.owner)
        self.db.commit()

        self.likes_url = (
            f'/api/v1/users/{self.owner.id}/posts/{self.post.id}/likes/'
        )

    @staticmethod
    def _get_like_unlike_link(
            user_id: int, post_id: int, action: like_unlike
    ) -> url:
        return (
            f'api/v1/users/{user_id}/posts/{post_id}/{action}/'
        )

    @staticmethod
    def _get_liked_users_link(user_id: int, post_id: int) -> url:
        return f'/api/v1/users/{user_id}/posts/{post_id}/likes/'

    def _get_test_post(
            self, user: models.User | None = None,
            likes: Iterable[models.User] | None = None
    ) -> models.Post:
        post = (
            PostFactory.create(likes=likes, user=user) if user is not None
            else PostFactory.create(likes=likes)
        )
        self.db.commit()

        return post

    def _refresh_posts(self, posts: Iterable[models.Post]) -> None:
        for post in posts:
            self.db.refresh(post)

    def _test_like_unlike_post_again(
            self, action: like_unlike
    ) -> None:
        headers = self._get_auth_headers(self.owner.username)

        test_post = (
            self._get_test_post(likes=(self.owner,)) if action == 'like'
            else self._get_test_post()
        )

        likes_count = test_post.likes_count
        response = self.client.post(
            self._get_like_unlike_link(test_post.user.id, test_post.id, action),
            headers=headers
        )

        self._refresh_posts((test_post,))
        new_likes_count = test_post.likes_count

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(likes_count, new_likes_count)

    def _test_get_liked_users_with_wrong_id(
            self, user_id: int, post_id: int
    ) -> None:
        response = self.client.get(
            self._get_liked_users_link(user_id, post_id)
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def _test_like_unlike_post(self, action: like_unlike) -> None:
        headers = self._get_auth_headers(self.owner.username)

        test_post = (
            self._get_test_post(likes=(self.owner,)) if action == 'unlike'
            else self._get_test_post()
        )

        likes_count = test_post.likes_count

        response = self.client.post(
            self._get_like_unlike_link(
                test_post.user.id, test_post.id, action
            ),
            headers=headers
        )

        self._refresh_posts((test_post,))
        new_likes_count = test_post.likes_count

        liked_users = PostInterface.get_liked_post_users(self.db, test_post.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if action == 'like':
            self.assertEqual(likes_count + 1, new_likes_count)
            self.assertIn(self.owner, liked_users)

        else:
            self.assertEqual(likes_count - 1, new_likes_count)
            self.assertNotIn(self.owner, liked_users)

    def test_get_post_liked_users(self) -> None:
        offset, limit = 3, 4

        serialized_users = [
            self._serialize_user(user)
            for user in self.liked_users[offset:offset + limit]
        ]

        response = self.client.get(
            self._get_liked_users_link(self.owner.id, self.post.id),
            params={'offset': offset, 'limit': limit}
        )
        received_content = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(received_content), limit)

        for received_user in received_content:
            self.assertIn(received_user, serialized_users)

    def test_get_post_liked_users_with_wrong_user(self) -> None:
        user_id, post_id = 555, self.post.id

        self._test_get_liked_users_with_wrong_id(user_id, post_id)

    def test_get_post_liked_users_with_wrong_post(self) -> None:
        user_id, post_id = self.owner.id, 555

        self._test_get_liked_users_with_wrong_id(user_id, post_id)

    def test_like_post(self) -> None:
        self._test_like_unlike_post('like')

    def test_like_post_again(self) -> None:
        self._test_like_unlike_post_again('like')

    def test_unlike_post(self) -> None:
        self._test_like_unlike_post('unlike')

    def test_unlike_post_again(self) -> None:
        self._test_like_unlike_post_again('unlike')


if __name__ == '__main__':
    unittest.main()
