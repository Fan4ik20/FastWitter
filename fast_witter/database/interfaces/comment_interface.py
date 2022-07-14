from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy.sql.selectable import Select

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
            select(models.Comment).filter_by(
                user_id=user_id
            ).offset(offset).limit(limit)
        ).all()

    @staticmethod
    def get_post_comments(
            db: Session, post_id: int,
            offset: int = 0, limit: int = 100
    ) -> list[models.Comment]:
        return db.scalars(
            select(models.Comment).filter_by(
                post_id=post_id
            ).offset(offset).limit(limit)
        ).all()

    @staticmethod
    def _get_post_comment_stmt(post_id: int, comment_id: int) -> Select:
        return select(models.Comment).filter_by(
            id=comment_id, post_id=post_id
        )

    @classmethod
    def get_post_comment_with_related(
            cls, db: Session, post_id: int, comment_id: int
    ) -> models.Comment | None:
        return db.scalar(
            cls._get_post_comment_stmt(post_id, comment_id).options(
                joinedload(models.Comment.post),
                joinedload(models.Comment.user)
            )
        )

    @classmethod
    def get_post_comment(
            cls, db: Session, post_id: int, comment_id: int
    ) -> models.Comment | None:
        return db.scalar(
            cls._get_post_comment_stmt(post_id, comment_id)
        )

    @staticmethod
    def _get_user_comment_stmt(user_id: int, comment_id: int) -> Select:
        return select(models.Comment).filter_by(
            id=comment_id, user_id=user_id
        )

    @classmethod
    def get_user_comment(
            cls, db: Session, user_id: int, comment_id: int
    ) -> models.Comment | None:

        return db.scalar(
            cls._get_user_comment_stmt(user_id, comment_id)
        )

    @classmethod
    def get_user_comment_with_related(
            cls, db: Session, user_id: int, comment_id: int
    ) -> models.Comment | None:
        return db.scalar(
            cls._get_user_comment_stmt(user_id, comment_id).options(
                joinedload(models.Comment.post),
                joinedload(models.Comment.user)
            )
        )

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
    def get_comment(db: Session, comment_id: int) -> models.Comment | None:
        return db.get(models.Comment, comment_id)

    @staticmethod
    def get_comment_with_related(
            db: Session, comment_id: int
    ) -> models.Comment | None:
        return db.scalar(
            select(models.Comment).filter_by(id=comment_id).options(
                joinedload(models.Comment.post),
                joinedload(models.Comment.user)
            )
        )

    @staticmethod
    def delete_comment(db: Session, comment: models.Comment) -> None:
        db.delete(comment)
        db.commit()
