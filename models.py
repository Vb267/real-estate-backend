from sqlalchemy import Column, Integer, String, Float
from database import Base


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    location = Column(String)
    size = Column(Float)
    image_url = Column(String)
