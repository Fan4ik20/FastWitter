import factory
from factory.alchemy import SQLAlchemyModelFactory

from database import models

from tests.service import test_session


class BaseSQLAlchemyFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = test_session
        sqlalchemy_session_persistence = 'commit'


class UserFactory(BaseSQLAlchemyFactory):

    class Meta:
        model = models.User
        sqlalchemy_get_or_create = ('username', 'email')

    username = factory.Faker('user_name')
    email = factory.Faker('ascii_email')
    hashed_password = factory.Faker('password')


class PostFactory(BaseSQLAlchemyFactory):
    class Meta:
        model = models.Post

    title = factory.Faker('sentence', nb_words=3)
    content = factory.Faker('sentence')

    user = factory.SubFactory(UserFactory)


class CommentFactory(BaseSQLAlchemyFactory):
    class Meta:
        model = models.Comment

    content = factory.Faker('sentence')

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
