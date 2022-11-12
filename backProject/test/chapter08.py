from typing import List, Optional

from fastapi import APIRouter, Form, File, UploadFile, HTTPException, Depends

app08 = APIRouter()




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

