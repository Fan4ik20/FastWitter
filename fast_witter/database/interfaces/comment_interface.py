from sqlalchemy import select
from sqlalchemy.orm import Session

from database import models
from schemas import comment_schemas as schemas


class CommentInterface:
    @staticmethod
    def get_all_comments(
            db: Session, offset: int = 0, limit: int = 100
    ) -> list[models.Comment]:

        return db.scalars(
            select(models.Comment).offset(offset).limit(limit)
        ).all()

    @staticmethod
    def get_users_comments(
            db: Session, user_id: int, offset: int = 0, limit: int = 100
    ) -> list[models.Comment]:

        return db.scalars(
            select(models.Post).filter_by(
                user_id=user_id
            ).offset(offset).limit(limit)
        ).all()

    @staticmethod
    def get_user_post_comments(
            db: Session, user_id: int, post_id: int,
            offset: int = 0, limit: int = 100
    ) -> list[models.Comment]:
        return db.scalars(
            select(models.Post).filter_by(
                user_id=user_id, post_id=post_id
            ).offset(offset).limit(limit)
        ).all()

    @staticmethod
    def get_user_post_comment(
            db: Session, user_id: int, post_id: int, comment_id: int
    ) -> models.Comment | None:
        return db.execute(
            select(models.Comment).filter_by(
                id=comment_id, user_id=user_id, post_id=post_id
            )
        ).scalar_one_or_none()

    @staticmethod
    def get_user_comment(
            db: Session, user_id: int, comment_id: int
    ) -> models.Comment | None:

        return db.execute(
            select(models.Comment).filter_by(
                id=comment_id, user_id=user_id
            )
        ).scalar_one_or_none()

    @staticmethod
    def create_comment(
            db: Session, owner_id: int, post_id: int,
            comment: schemas.CommentCreate
    ) -> models.Comment:
        new_comment = models.Comment(
            user_id=owner_id, post_id=post_id, **comment.dict()
        )

        db.add(new_comment)
        db.commit()

        db.refresh(new_comment)

        return new_comment

    @staticmethod
    def get_comment(db: Session, comment_id) -> models.Comment | None:
        return db.get(models.Comment, comment_id)

    @staticmethod
    def delete_comment(db: Session, comment: models.Comment) -> None:
        db.delete(comment)
        db.commit()
