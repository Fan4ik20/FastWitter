from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, subqueryload
from sqlalchemy.sql.selectable import Select

from database import models
from schemas import post_schemas as schemas


class PostInterface:
    @staticmethod
    def get_all_posts(
            db: Session, skip: int = 0, limit: int = 100
    ) -> list[models.Post]:

        return db.scalars(
            select(models.Post).offset(skip).limit(limit)
        ).all()

    @staticmethod
    def get_users_posts(
            db: Session, user_id: int, offset: int = 0, limit: int = 100
    ) -> list[models.Post]:
        return db.scalars(
            select(models.Post).filter_by(
                user_id=user_id
            ).offset(offset).limit(limit)
        ).all()

    @staticmethod
    def _get_user_post_stmt(user_id: int, post_id: int) -> Select:
        return select(models.Post).filter_by(id=post_id, user_id=user_id)

    @classmethod
    def get_user_post(
            cls, db: Session, user_id: int, post_id: int
    ) -> models.Post | None:
        return db.scalar(
            cls._get_user_post_stmt(user_id, post_id)
        )

    @classmethod
    def get_user_post_with_related(
            cls, db: Session, user_id: int, post_id: int
    ) -> models.Post | None:
        return db.scalar(
            cls._get_user_post_stmt(user_id, post_id).options(
                joinedload(models.Post.user)
            )
        )

    @staticmethod
    def create_post(
            db: Session, post: schemas.PostCreate, user_id: int
    ) -> models.Post:

        post = models.Post(**post.dict(), user_id=user_id)

        db.add(post)
        db.commit()

        db.refresh(post)

        return post

    @staticmethod
    def get_post(db: Session, post_id: int) -> models.Post | None:
        return db.get(models.Post, post_id)

    @staticmethod
    def get_post_with_related(db: Session, post_id: int) -> models.Post | None:
        return db.scalar(
            select(models.Post).filter_by(id=post_id).options(
                joinedload(models.Post.user)
            )
        )

    @staticmethod
    def increase_likes_count(db: Session, post: models.Post) -> None:
        post.likes_count += 1
        db.commit()

    @staticmethod
    def decrease_likes_count(db: Session, post: models.Post) -> None:
        post.likes_count -= 1
        db.commit()

    @staticmethod
    def is_user_liked_post(db: Session, user_id: int, post_id: int) -> bool:
        return db.query(
            select(models.Post).filter(
                models.Post.id == post_id,
                models.Post.likes.any(models.User.id == user_id)
            ).exists()
        ).scalar()

    @staticmethod
    def get_liked_post_users(
            db: Session, post_id: int, offset: int = 0, limit: int = 100
    ) -> list[models.User]:
        return db.scalars(
            select(models.User).filter(
                models.User.liked_posts.any(models.Post.id == post_id)
            ).options(
                subqueryload(models.User.liked_posts)
            ).offset(offset).limit(limit)
        ).all()

    @classmethod
    def like_post(
            cls, db: Session, post: models.Post, user: models.User
    ) -> None:
        post.likes.append(user)
        db.commit()

        cls.increase_likes_count(db, post)

    @classmethod
    def unlike_post(
            cls, db: Session, post: models.Post, user: models.User
    ) -> None:
        post.likes.remove(user)
        db.commit()

        cls.decrease_likes_count(db, post)

    @staticmethod
    def delete_post(db: Session, post: models.Post) -> None:
        db.delete(post)
        db.commit()
