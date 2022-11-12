from typing import List, Optional

from fastapi import APIRouter, Form, File, UploadFile, HTTPException, Depends

app08 = APIRouter()

"""Form Data 表单数据处理"""


@app08.post('login')
async def login(username: str = Form(...),
                password: str = Form(...)):
    return {'username': username}


"""Request Files 单文件、多文件上传及参数详解"""


@app08.post('/file')
async def file_(file: bytes = File(...)):
    """
    使用File类，文件内容会以bytes的形式读入内存。适合于上传小文件
    :param file: 上传文件
    :return: 文件大小
    """
    return {'file_size': len(file)}


@app08.post('/Upload_files')
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


# @app08.get('/http_exception')
# async def http_exception(city: str):
#     if city != 'Beijing':
#         raise HTTPException(status_code=404,
#                             detail='City not found!',
#                             headers={'X-Error': 'Error'})
#     return {'city': city}
#
#
# @app08.get('/override_http_exception')
# async def override_http_exception(city_id: int):
#     if city_id == 1:
#         raise HTTPException(status_code=418,
#                             detail="Nope! I don't like 1.",
#                             headers={'X-Error': 'Error'})
#     return {'city': city_id}


"""Dependencies 创建，导入和声明依赖"""


async def common_parameters(q: Optional[str] = None,
                            page: int = 1,
                            limit: int = 100):
    return {'q': q, 'page': page, 'limit': limit}


@app08.get('/dependency')
async def dependency(commons: dict = Depends(common_parameters)):
    return commons


"""Classes as Dependencies 类作为依赖项"""


fake_items_db = [{'item_name': 'Foo'}, {'item_name': 'Bar'}, {'item_name ': 'Baz'}]


class CommonQueryParams:
    def __init__(self, q: Optional[str] = None,
                            page: int = 1,
                            limit: int = 100):
        self.q = q
        self.page = page
        self.limit = limit


@app08.get('/classes_as_dependencies')
async def classes_as_dependencies(commons=Depends(CommonQueryParams)):
    response = {}

