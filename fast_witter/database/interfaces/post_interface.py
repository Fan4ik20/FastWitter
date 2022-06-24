from sqlalchemy import select
from sqlalchemy.orm import Session

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
    def get_user_post(
            db: Session, user_id: int, post_id: int
    ) -> models.Post | None:
        return db.execute(
            select(models.Post).filter_by(id=post_id, user_id=user_id)
        ).scalar_one_or_none()

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
    def increase_likes_count(db: Session, post: models.Post) -> None:
        post.likes_count += 1
        db.commit()

    @staticmethod
    def decrease_likes_count(db: Session, post: models.Post) -> None:
        post.likes_count -= 1
        db.commit()

    @staticmethod
    def like_post(db: Session, post: models.Post, user: models.User) -> None:
        post.likes.append(user)
        db.commit()

        PostInterface.increase_likes_count(db, post)

    @staticmethod
    def unlike_post(db: Session, post: models.Post, user: models.User) -> None:
        post.likes.remove(user)
        db.commit()

        PostInterface.decrease_likes_count(db, post)

    @staticmethod
    def delete_post(db: Session, post: models.Post) -> None:
        db.delete(post)
        db.commit()
