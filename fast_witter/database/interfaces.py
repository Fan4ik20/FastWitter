from sqlalchemy import select
from sqlalchemy.orm import Session

from database import models
import schemas
from security import service


class UserInterface:
    @staticmethod
    def get_users(
            db: Session, skip: int = 0, limit: int = 100
    ) -> list[models.User]:

        return db.execute(
            select(
                models.User
            ).offset(skip).limit(limit)
        ).scalars().all()

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
    def get_user(db: Session, id_: int) -> models.User:
        return db.get(models.User, id_)

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> models.User:
        return db.execute(
            select(models.User).filter_by(email=email)
        ).first()
