import unittest

from fastapi import status

from tests.factories import CommentFactory, UserFactory
from tests.base import CommentTestBase


class TestUserCommentsRoutes(CommentTestBase):
    def setUp(self) -> None:
        super().setUp()

        self.user = UserFactory(username='TEST')
        self.user_comments = [
            CommentFactory(user=self.user) for _ in range(10)
        ]

        self.comments_url = f'/api/v1/users/{self.user.id}/comments'

    def test_get_user_comments(self) -> None:
        offset, limit = 2, 5

        serialized_comments = [
            self._serialize_comment(comment)
            for comment in self.user_comments[offset: offset + limit]
        ]

        response = self.client.get(
            f'{self.comments_url}/', params={'offset': offset, 'limit': limit}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for received_comment in response.json():
            self.assertIn(received_comment, serialized_comments)

    def test_get_user_comments_with_wrong_user_id(self) -> None:
        user_id = 555

        response = self.client.get(f'/api/v1/users/{user_id}/comments/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_comment(self) -> None:
        for comment in self.user_comments:
            serialized_comment = self._serialize_detailed_comment(comment)

            response = self.client.get(f'{self.comments_url}/{comment.id}/')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json(), serialized_comment)

    def test_get_user_comment_with_wrong_id(self) -> None:
        invalid_id = 404

        response = self.client.get(f'{self.comments_url}/{invalid_id}/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_user_comment(self) -> None:
        headers = self._get_auth_headers(self.user.username)

        for comment in self.user_comments:
            response = self.client.delete(
                f'{self.comments_url}/{comment.id}/', headers=headers
            )

            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_comment_unauthorized(self) -> None:
        for comment in self.user_comments:
            response = self.client.delete(
                f'{self.comments_url}/{comment.id}/'
            )

            self.assertEqual(
                response.status_code, status.HTTP_401_UNAUTHORIZED
            )

    def test_delete_user_comment_with_wrong_user(self) -> None:
        test_user = UserFactory(username='TestDelete')

        headers = self._get_auth_headers(test_user.username)

        for comment in self.user_comments:
            response = self.client.delete(
                f'{self.comments_url}/{comment.id}/', headers=headers
            )

            self.assertEqual(
                response.status_code, status.HTTP_403_FORBIDDEN
            )


if __name__ == '__main__':
    unittest.main()
