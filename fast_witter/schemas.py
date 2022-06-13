from pydantic import BaseModel, Field, PositiveInt, EmailStr


class UserBase(BaseModel):
    username: str = Field(..., max_length=30)
    email: EmailStr
    name: str | None = Field(None, max_length=20)
    surname: str | None = Field(None, max_length=30)


class UserLogin(BaseModel):
    username: str = Field(..., max_length=30)
    password: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: PositiveInt

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str = Field(..., max_length=30)
    content: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: PositiveInt

    likes_count: int

    user_id: int = Field(..., ge=1)

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    content: str = Field(..., max_length=100)


class CommentCreate(BaseModel):
    pass


class Comment(CommentBase):
    id: PositiveInt

    user_id: PositiveInt
    post_id: PositiveInt

    class Config:
        orm_mode = True
