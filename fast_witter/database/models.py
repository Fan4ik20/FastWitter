from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from fast_witter.database.settings import blog_engine

BlogBase = declarative_base()


subscribers = Table(
    'subscribers', BlogBase.metadata,
    Column("first_user_id", Integer, ForeignKey('users.id'), primary_key=True),
    Column("second_user_id", Integer, ForeignKey('users.id'), primary_key=True)
)

likes = Table(
    'likes', BlogBase.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True)
)


class User(BlogBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), nullable=False)
    email = Column(String(30), nullable=False)
    hashed_password = Column(String(30), nullable=False)

    name = Column(String(20))
    surname = Column(String(30))

    subscribers = relationship(
        'User', secondary=subscribers, backref='subscribed'
    )


class Post(BlogBase):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(10), nullable=False)
    content = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', backref='posts')
    likes = relationship('User', secondary=likes, backref='liked_posts')


class Comment(BlogBase):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    content = Column(String(30), nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)

    user = relationship('User', backref='comments')
    post = relationship('Post', backref='comments')
