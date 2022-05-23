from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database import models
import schemas
from security import service


class UserInterface:
    @staticmethod
    def get_users(
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
    def get_user_by_email(db: Session, email: str) -> models.User:
        return db.scalars(
            select(models.User).filter_by(email=email)
        ).first()

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
            select(models.Post).filter_by(user_id=user_id, post_id=post_id)
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
    def delete_post(db: Session, post_id: int) -> bool | None:
        post = db.execute(
            select(models.Post).filter_by(id=post_id)
        ).scalar_one_or_none()

        if post is None:
            return None

        db.delete(post)
        db.commit()

        return True
