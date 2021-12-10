from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str
    email: str


class UserCreate(BaseUser):
    password: str


class UserUpdate(BaseUser):
    pass


class User(BaseUser):
    id: int
    surname: str
    description: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
