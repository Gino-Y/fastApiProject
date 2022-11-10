"""
响应体校验
"""
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

app04 = APIRouter()


class UserBase(BaseModel):
    username: str
    email: EmailStr
    mobile: str = '10086'
    address: str = None
    full_name: Optional[str] = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


users = {
    'user01': {'username': 'user01',
               'password': '123123',
               'email': 'user01@example.com'},
    'user02': {'username': 'user02',
               'password': '123123',
               'email': 'user01@example.com'},
        }


@app04.post('/response_model', response_model=UserOut, response_model_exclude_none=True)
async def response_model(user: UserIn):
    print(user.password)


