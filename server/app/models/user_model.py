from pydantic import BaseModel


class User(BaseModel):
    preferences: dict
