from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str
    email: str
    name: str | None = None
    surname: str | None = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int = Field(..., ge=1)

    class Config:
        orm_mode = True


class Comment(BaseModel):
    class Config:
        orm_mode = True


class Post(BaseModel):
    class Config:
        orm_mode = True
