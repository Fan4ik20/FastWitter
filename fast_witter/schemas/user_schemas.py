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


class UserBuiltin(BaseModel):
    id: PositiveInt
    username: str = Field(..., max_length=30)

    class Config:
        orm_mode = True
