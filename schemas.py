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
