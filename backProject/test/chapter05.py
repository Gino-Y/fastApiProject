from fastapi import APIRouter, Depends, Header, HTTPException
from typing import Optional

app05 = APIRouter()

"""Dependencies 创建、导入和声明依赖"""


async def common_parameters(q: Optional[str] = None,
                            page: int = 1,
                            limit: int = 100):
    return {'q': q, 'page': page, 'limit': limit}


@app05.get('/dependency')
async def dependency(commons: dict = Depends(common_parameters)):
    return commons


"""Classes as Dependencies 类作为依赖项"""

fake_items_db = [{'item_name': 'Foo'}, {'item_name': 'Bar'}, {'item_name ': 'Baz'}]


class CommonQueryParams:
    def __init__(self, q: Optional[str] = None,
                 page: int = 0,
                 limit: int = 100):
        self.q = q
        self.page = page
        self.limit = limit


@app05.get('/classes_as_dependencies')
async def classes_as_dependencies(commons=Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({'q': commons.q})
    items = fake_items_db[commons.page: commons.page + commons.limit]
    response.update({'items': items})
    return response


"""Sub-dependencies 子依赖"""


async def query(q: Optional[str] = None):
    return q


async def sub_query(q: str = Depends(query), last_query: Optional[str] = None):
    if not q:
        return last_query
    return q


@app05.get('/sub_dependency')
async def sub_dependency(final_query: str = Depends(sub_query, use_cache=True)):
    return {'sub_dependency': final_query}


"""Dependencies in path operation decorators 路径操作装饰器中的依赖"""


async def verify_token(x_token: str = Header(...)):
    """没有返回值的子依赖"""
    if x_token != 'fake-suber-secret-token':
        raise HTTPException(status_code=400, detail='X-Token header invalid')
    return x_token


async def verify_key(x_key: str = Header(...)):
    """有有返回值的子依赖，但是返回值不会被调用"""
    if x_key != 'fake-suber-secret-key':
        raise HTTPException(status_code=400, detail='X-key header invalid')
    return x_key


@app05.get('/dependency_in_path_operation', dependencies=[Depends(verify_token), Depends(verify_key)])
async def dependency_in_path_operation():
    return [{'user': 'user01'}, {'user': 'user02'}]


"""Global Dependencies 全局依赖"""

# @app05 = APIRouter(dependencies=[Depends(verify_token), Depends(verify_key)])


"""Dependencies with yield 带yield的依赖"""

# 5-7



















