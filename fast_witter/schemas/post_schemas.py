from pydantic import BaseModel, Field, PositiveInt

from schemas.user_schemas import UserBuiltin


class PostBase(BaseModel):
    title: str = Field(..., max_length=30)
    content: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: PositiveInt

    likes_count: int

    user_id: PositiveInt

    class Config:
        orm_mode = True


class PostDetail(PostBase):
    id: PositiveInt

    likes_count: int

    user: UserBuiltin = Field(..., alias='owner',)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
