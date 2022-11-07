"""
响应体校验
"""
from typing import Optional, Union, List

from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from starlette import status

app04 = APIRouter()


class UserBase(BaseModel):
    username: str
    email: EmailStr
    mobile: str = '10086'
    address: str = None
    full_name: Optional[str] = None


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    mobile: str = '10086'
    address: str = None
    full_name: Optional[str] = None

    class Config:
        schema_extra = {
            'user01': {'username': 'user01',
                       'password': '123123',
                       'email': 'user01@example.com',
                       'mobile': '110'},
        }


class UserOut(BaseModel):
    username: str
    email: EmailStr
    mobile: str = '10086'
    address: str = None
    full_name: Optional[str] = None

    class Config:
        schema_extra = {
            'user01': {'username': 'user01',
                       'email': 'user01@example.com',
                       'mobile': '110'},
        }


users = {
    'user01': {'username': 'user01',
               'password': '123123',
               'email': 'user01@example.com'},
    'user02': {'username': 'user02',
               'password': '123123',
               'email': 'user01@example.com',
               'mobile': '110'},
}


@app04.post('/response_model', response_model=UserOut, response_model_exclude_unset=True)
async def response_model(user: UserIn):
    # print(user.password)
    return users['user02']


@app04.post('response_model/attributes',
            # response_model=UserOut,
            # response_model=Union[UserIn, UserOut],
            response_model=List[UserOut],
            # response_model_include=['username'],
            # response_model_exclude=['password'],
            )
async def response_model_attributes(user: UserIn):
    del user.password
    return [user, user]


"""Response status Code 响应状态码"""


@app04.post('/status_code', status_code=200)
async def status_code():
    return {'status_code': 200}


@app04.post('/status_attribute', status_code=status.HTTP_200_OK)
async def status_attribute():
    return {'status_code': status.HTTP_200_OK}
