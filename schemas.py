from pydantic import BaseModel


class PropertyBase(BaseModel):
    title: str
    description: str
    price: float
    location: str
    size: float
    image_url: str


class PropertyCreate(PropertyBase):
    pass


class Property(PropertyBase):
    id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
