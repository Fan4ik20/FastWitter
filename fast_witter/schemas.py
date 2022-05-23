from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(..., max_length=30)
    email: str = Field(..., max_length=30)
    name: str | None = Field(None, max_length=20)
    surname: str | None = Field(None, max_length=30)


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int = Field(..., ge=1)

    class Config:
        orm_mode = True


class Comment(BaseModel):
    class Config:
        orm_mode = True


class PostModel(BaseModel):
    title: str = Field(..., max_length=10)
    content: str


class PostCreate(PostModel):
    pass


class Post(PostCreate):
    id: int = Field(..., ge=1)

    user_id: int = Field(..., ge=1)

    class Config:
        orm_mode = True
