import datetime as dt
from pydantic import BaseModel
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    hashed_password: str

class User(UserBase):
    id: int

    class Config:
        model_config = {'from_attributes': True}

class TaskBase(BaseModel):

    name : str
    situation: str

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id : int
    owner_id : int
    situation: str
    date_created : dt.datetime
    date_last_updated : dt.datetime
    date_start : dt.datetime
    date_end : dt.datetime

    class Config:
        model_config = {'from_attributes': True}
        use_enum_values = True
        populate_by_name = True
        use_enum_values = True
        arbitrary_types_allowed = True