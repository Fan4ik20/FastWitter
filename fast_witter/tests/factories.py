import factory
from factory.alchemy import SQLAlchemyModelFactory

from sqlalchemy.orm import scoped_session

from database import models

from tests.service import TestSession

factory_session = scoped_session(TestSession)


class UserFactory(SQLAlchemyModelFactory):

    class Meta:
        model = models.User
        sqlalchemy_session = factory_session
        sqlalchemy_get_or_create = ('username', 'email')
        sqlalchemy_session_persistence = 'commit'

    username = factory.Faker('user_name')
    email = factory.Faker('ascii_email')
    hashed_password = factory.Faker('password')
