import unittest

from fastapi import status

from tests.base import PostTestBase
from tests.factories import UserFactory, PostFactory


class TestUserPostsRoutes(PostTestBase):
    def setUp(self) -> None:
        super().setUp()

        self.user = UserFactory(username='TEST')
        self.user_posts = [PostFactory(user=self.user) for _ in range(10)]

    def test_get_user_posts(self) -> None:
        serialized_posts = [
            self._serialize_post(post) for post in self.user_posts
        ]
        print(serialized_posts)

        response = self.client.get(
            f'/api/v1/users/{self.user.id}/posts/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for received_json in response.json():
            self.assertIn(received_json, serialized_posts)

    def test_get_user_posts_with_invalid_user_id(self) -> None:
        invalid_id = 404

        response = self.client.get(f'/api/v1/users/{invalid_id}/posts/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_get_user_post(self) -> None:
        for post in self.user_posts:
            serialized_post = self._serialize_detailed_post(post)

            response = self.client.get(
                f'/api/v1/users/{self.user.id}/posts/{post.id}/'
            )

            with self.subTest():
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.json(), serialized_post)

    def test_get_user_post_with_invalid_post_id(self) -> None:
        invalid_ids = [404, 202, 555]

        for id_ in invalid_ids:
            response = self.client.get(
                f'/api/v1/users/{self.user.id}/posts/{id_}/'
            )

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_user_post(self) -> None:
        token = self._generate_token(self.user.username)

        headers = {'Authorization': f'Bearer {token}'}

        for post in self.user_posts:
            response = self.client.delete(
                f'/api/v1/users/{self.user.id}/posts/{post.id}/',
                headers=headers
            )

            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post_with_wrong_user(self) -> None:
        test_post = PostFactory()

        token = self._generate_token(self.user.username)

        headers = {'Authorization': f'Bearer {token}'}

        response = self.client.delete(
            f'/api/v1/users/{test_post.user.id}/posts/{test_post.id}/',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


if __name__ == '__main__':
    unittest.main()
