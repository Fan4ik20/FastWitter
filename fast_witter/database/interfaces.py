from sqlalchemy import select
from sqlalchemy.orm import Session

from database import models, settings
import schemas
from security import service


class DbInterface:
    @staticmethod
    def create_tables() -> None:
        models.BlogBase.metadata.create_all(bind=settings.blog_engine)


class UserInterface:
    @staticmethod
    def get_all_users(
            db: Session, skip: int = 0, limit: int = 100
    ) -> list[models.User]:

        return db.scalars(
            select(
                models.User
            ).offset(skip).limit(limit)
        ).all()

    @staticmethod
    def get_user(db: Session, id_: int) -> models.User | None:
        return db.get(models.User, id_)

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> models.User | None:
        return db.execute(
            select(models.User).filter_by(username=username)
        ).scalar_one_or_none()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> models.User | None:
        return db.execute(
            select(models.User).filter_by(email=email)
        ).scalar_one_or_none()

    @staticmethod
    def create_user(db: Session, user: schemas.UserCreate) -> models.User:
        hashed_password = service.get_password_hash(user.password)

        db_user = models.User(
            username=user.username,
            email=user.email, hashed_password=hashed_password,
            name=user.name, surname=user.surname
        )

        db.add(db_user)
        db.commit()

        db.refresh(db_user)

        return db_user


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
    def delete_post(db: Session, post: models.Post) -> None:
        db.delete(post)
        db.commit()


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
            db: Session, user_id: int, post_id: int,
            comment: schemas.CommentCreate
    ) -> models.Comment:
        new_comment = models.Comment(
            user_id=user_id, post_id=post_id, **comment.dict()
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
