from pydantic import BaseModel, Field, PositiveInt

from schemas.user_schemas import UserBuiltin
from schemas.post_schemas import Post


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


class CommentDetail(CommentBase):
    id: PositiveInt

    user: UserBuiltin = Field(..., alias='owner')
    post: Post

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
