"""
响应体校验
"""
from typing import List, Optional

from fastapi import APIRouter, Form, File, UploadFile, HTTPException, Depends
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


"""Form Data 表单数据处理"""


@app04.post('login')
async def login(username: str = Form(...),
                password: str = Form(...)):
    return {'username': username}


"""Request Files 单文件、多文件上传及参数详解"""


@app04.post('/file')
async def file_(file: bytes = File(...)):
    """
    使用File类，文件内容会以bytes的形式读入内存。适合于上传小文件
    :param file: 上传文件
    :return: 文件大小
    """
    return {'file_size': len(file)}


@app04.post('/Upload_files')
async def Upload_files(files: List[UploadFile] = File(...)):
    """
    使用UploadFile类的优势：
    1、文件存储在内存张洪，使用的内存达到阈值后，将被保存在磁盘中
    2、适合于图片，视频大文件
    3、可以获取上传的文件的元数据，如文件名，创建时间等
    4、有文件对象的异步接口
    5、上传的文件时Python文件对象，可以使用write(), read(), seek(), close()操作
    :param files: 上传文件
    :return:
    """
    for file in files:
        contents = file.read()
        print(contents)

    return {'file_size': files[0].filename,
            'content_type': files[0].content_type}


"""【见main.py】FastAPI 应用的常见配置项"""

"""Handling Errors 错误处理"""


# @app04.get('/http_exception')
# async def http_exception(city: str):
#     if city != 'Beijing':
#         raise HTTPException(status_code=404,
#                             detail='City not found!',
#                             headers={'X-Error': 'Error'})
#     return {'city': city}
#
#
# @app04.get('/override_http_exception')
# async def override_http_exception(city_id: int):
#     if city_id == 1:
#         raise HTTPException(status_code=418,
#                             detail="Nope! I don't like 1.",
#                             headers={'X-Error': 'Error'})
#     return {'city': city_id}


