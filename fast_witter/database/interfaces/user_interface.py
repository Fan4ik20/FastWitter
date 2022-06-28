from sqlalchemy import select
from sqlalchemy.orm import Session, subqueryload
from sqlalchemy.sql.selectable import Select

from database import models
from schemas import user_schemas as schemas
from security import service


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
    def get_user(db: Session, user_id: int) -> models.User | None:
        return db.get(models.User, user_id)

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

    @staticmethod
    def _increase_user_followers_count(db: Session, user: models.User) -> None:
        user.followers_count += 1
        db.commit()

    @staticmethod
    def _decrease_user_followers_count(db: Session, user: models.User) -> None:
        user.followers_count -= 1
        db.commit()

    @staticmethod
    def _increase_user_following_count(db: Session, user: models.User) -> None:
        user.following_count += 1
        db.commit()

    @staticmethod
    def _decrease_user_following_count(db: Session, user: models.User) -> None:
        user.following_count -= 1
        db.commit()

    @classmethod
    def follow_user(
            cls, db: Session, followed: models.User, follower: models.User
    ) -> None:

        followed.followers.append(follower)
        db.commit()

        cls._increase_user_followers_count(db, followed)
        cls._increase_user_following_count(db, follower)

    @classmethod
    def unfollow_user(
            cls, db: Session, followed: models.User, follower: models.User
    ) -> None:
        followed.followers.remove(follower)
        db.commit()

        cls._decrease_user_followers_count(db, followed)
        cls._decrease_user_following_count(db, follower)

    @staticmethod
    def get_user_with_related(db: Session, user_id: int) -> models.User | None:
        return db.scalar(
            select(models.User).filter_by(id=user_id).options(
                subqueryload(models.User.following)
            )
        )

    @staticmethod
    def _get_user_followers_stmt(user_id: int) -> Select:
        return select(models.User).filter(
            models.User.following.any(models.User.id == user_id)
        )

    @classmethod
    def get_user_followers(
            cls, db: Session, user_id: int, offset: int = 0, limit: int = 100
    ) -> list[models.User]:
        return db.scalars(
            cls._get_user_followers_stmt(user_id).offset(offset).limit(limit)
        ).all()

    @classmethod
    def is_user_followed(
            cls, db: Session, followed_id: int, follower_id: int
    ) -> bool:
        return db.query(
            cls._get_user_followers_stmt(
                followed_id
            ).filter_by(id=follower_id).exists()
        ).scalar()

    @staticmethod
    def get_user_following(
            db: Session, user_id, offset: int = 0, limit: int = 100
    ) -> list[models.User]:
        return db.scalars(
            select(models.User).filter(
                models.User.followers.any(models.User.id == user_id)
            ).offset(offset).limit(limit)
        ).all()
