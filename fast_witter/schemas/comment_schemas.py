from pydantic import BaseModel, Field, PositiveInt


class CommentBase(BaseModel):
    content: str = Field(..., max_length=100)


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: PositiveInt

    user_id: PositiveInt
    post_id: PositiveInt

    class Config:
        orm_mode = True
