import unittest

from fastapi import status

from tests.base import PostTestBase
from tests.factories import PostFactory, UserFactory

from database import models
from database.interfaces.post_interface import PostInterface


class TestPostsRoutes(PostTestBase):
    def setUp(self) -> None:
        super().setUp()
        
        self.posts = [PostFactory() for _ in range(10)]

    def test_get_posts(self) -> None:
        limit = 7

        serialized_posts = [
            self._serialize_post(post) for post in self.posts[:limit]
        ]

        response = self.client.get(
            '/api/v1/posts/', params={'limit': limit}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        received_content = response.json()

        self.assertEqual(len(received_content), limit)
        for received_post in received_content:
            self.assertIn(received_post, serialized_posts)

    def test_create_post(self) -> None:
        post_owner: models.User = UserFactory(username='TEST')
        token = self._generate_token(post_owner.username)

        payload = {'title': 'TestTitle', 'content': 'TestContent'}
        headers = {'Authorization': f'Bearer {token}'}

        response = self.client.post(
            '/api/v1/posts/', json=payload, headers=headers
        )
        received_content = response.json()

        created_post = PostInterface.get_users_posts(self.db, post_owner.id)[0]

        expected_json = {
            'id': created_post.id, 'user_id': post_owner.id, 'likes_count': 0
        }
        expected_json = expected_json | payload

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(received_content, expected_json)

    def test_create_post_with_long_title(self) -> None:
        post_owner: models.User = UserFactory(username='TEST')
        token = self._generate_token(post_owner.username)

        payload = {'title': 'a' * 35, 'content': 'TestContent'}
        headers = {'Authorization': f'Bearer {token}'}

        response = self.client.post(
            '/api/v1/posts/', json=payload, headers=headers
        )
        self.assertEqual(
            response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    def test_get_post(self) -> None:
        post_ids = [1, 3, 5]

        for id_ in post_ids:
            post = PostInterface.get_post(self.db, id_)
            serialized_post = self._serialize_detailed_post(post)

            response = self.client.get(
                f'/api/v1/posts/{id_}/'
            )

            with self.subTest():
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.json(), serialized_post)

    def test_get_post_with_invalid_id(self) -> None:
        invalid_ids = [-100, 2220, 334]

        for id_ in invalid_ids:
            response = self.client.get(f'/api/v1/posts/{id_}/')

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


if __name__ == '__main__':
    unittest.main()
