from sqlalchemy import select
from sqlalchemy.orm import Session

from database import models
import schemas
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