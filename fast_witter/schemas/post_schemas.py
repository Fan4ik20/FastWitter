from pydantic import BaseModel, Field, PositiveInt


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
