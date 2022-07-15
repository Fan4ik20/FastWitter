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

    @factory.post_generation
    def following(self: models.User, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for followed in extracted:
                self.following.append(followed)

                self.following_count += 1
                followed.followers_count += 1


class PostFactory(BaseSQLAlchemyFactory):
    class Meta:
        model = models.Post

    title = factory.Faker('sentence', nb_words=3, variable_nb_words=False)
    content = factory.Faker('sentence')

    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def likes(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for like in extracted:
                self.likes.append(like)


class CommentFactory(BaseSQLAlchemyFactory):
    class Meta:
        model = models.Comment

    content = factory.Faker('sentence')

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
