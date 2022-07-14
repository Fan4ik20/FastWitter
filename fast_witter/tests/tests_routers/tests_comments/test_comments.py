import unittest

from fastapi import status

from tests.base import CommentTestBase
from tests.factories import CommentFactory


class TestCommentsRoutes(CommentTestBase):
    def setUp(self) -> None:
        super().setUp()

        self.comments = [CommentFactory() for _ in range(10)]

    def test_get_comments(self) -> None:
        limit = 5

        serialized_comments = [
            self._serialize_comment(comment)
            for comment in self.comments[:limit]
        ]

        response = self.client.get(
            '/api/v1/comments/', params={'limit': limit}
        )
        received_content = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(received_content), limit)

        for received_comment in received_content:
            self.assertIn(received_comment, serialized_comments)

    def test_get_ind_comment(self) -> None:
        for comment in self.comments:
            serialized_comment = self._serialize_detailed_comment(comment)

            response = self.client.get(f'/api/v1/comments/{comment.id}/')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json(), serialized_comment)

    def test_get_ind_comment_with_wrong_id(self) -> None:
        invalid_ids = [202, 404, 555]

        for id_ in invalid_ids:
            response = self.client.get(f'/api/v1/comments/{id_}/')

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


if __name__ == '__main__':
    unittest.main()
