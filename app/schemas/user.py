from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    # not forced to always update all the fields
    username: Optional[str]=None
    email: EmailStr 
    password: str 

    model_config = ConfigDict(from_attributes=True)


class UserReturn(UserBase):
    id: int
    created_at: datetime
