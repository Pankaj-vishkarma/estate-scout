from pydantic import BaseModel


class Property(BaseModel):
    title: str
    price: str
    address: str
    image: str
