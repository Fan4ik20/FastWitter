import unittest

from fastapi import status

from database.interfaces.comment_interface import CommentInterface
from database.interfaces.user_interface import UserInterface

from tests.base import CommentTestBase
from tests.factories import CommentFactory, PostFactory, UserFactory


class TestPostCommentsRoutes(CommentTestBase):
    def setUp(self) -> None:
        super().setUp()

        self.user = UserFactory(username='TEST')
        self.post = PostFactory(user=self.user)
        self.post_comments = [
            CommentFactory(post=self.post) for _ in range(10)
        ]

        self.comments_url = (
            f'/api/v1/users/{self.user.id}/posts/{self.post.id}/comments'
        )

    def test_get_post_comments(self) -> None:
        serialized_comments = [
            self._serialize_comment(comment) for comment in self.post_comments
        ]

        response = self.client.get(f'{self.comments_url}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for received_comment in response.json():
            self.assertIn(received_comment, serialized_comments)

    def test_get_post_comments_with_non_existing_user(self) -> None:
        user_id = 404

        response = self.client.get(
            f'/api/v1/users/{user_id}/posts/{self.post.id}/comments/'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def tests_get_post_comments_with_non_existing_post(self) -> None:
        post_id = 34

        response = self.client.get(
            f'/api/v1/users/{self.user.id}/posts/{post_id}/comments'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_comment(self) -> None:
        payload = {'content': 'test comment content'}
        headers = self._get_auth_headers(self.user.username)

        response = self.client.post(
            f'{self.comments_url}/', json=payload, headers=headers
        )
        received_content = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_comment = CommentInterface.get_post_comment(
            self.db, self.post.id, received_content['id']
        )
        with self.subTest():
            self.assertEqual(created_comment.content, payload['content'])
            self.assertEqual(created_comment.user_id, self.user.id)
            self.assertEqual(created_comment.post_id, self.post.id)

    def test_create_comment_non_authorized(self) -> None:
        payload = {'content': 'NON AUTHORIZED'}

        response = self.client.post(f'{self.comments_url}/', json=payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_post_comment(self) -> None:
        for comment in self.post_comments:
            serialized_comment = self._serialize_detailed_comment(comment)

            response = self.client.get(f'{self.comments_url}/{comment.id}/')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json(), serialized_comment)

    def test_get_post_comment_with_invalid_id(self) -> None:
        invalid_id = 404

        response = self.client.get(f'{self.comments_url}/{invalid_id}/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_comment(self):
        user_comment = CommentFactory(user=self.user, post=self.post)

        headers = self._get_auth_headers(self.user.username)

        response = self.client.delete(
            f'{self.comments_url}/{user_comment.id}/', headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_comment_by_post_owner(self) -> None:
        headers = self._get_auth_headers(self.user.username)

        for comment in self.post_comments:
            response = self.client.delete(
                f'{self.comments_url}/{comment.id}/', headers=headers
            )

            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_comment_by_wrong_user(self) -> None:
        test_comment = self.post_comments[0]
        test_user = UserFactory(username='TestDELETE')

        headers = self._get_auth_headers(test_user.username)

        response = self.client.delete(
            f'{self.comments_url}/{test_comment.id}/', headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


if __name__ == '__main__':
    unittest.main()
