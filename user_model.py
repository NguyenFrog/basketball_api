from bson import ObjectId
from pydantic import BaseModel


class User(BaseModel):
    _id = ObjectId
    username: str
    hashed_password: str
    is_admin: bool

    def __getitem__(self, item):
        return self.__dict__[item]
