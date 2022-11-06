"""
****请求校验
使用pydantic定义请求体数据时，要使用Field()类对字段进行校验
路径参数校验使用Path()类
查询参数校验使用Query()类

"""
from typing import Optional, List
from pydantic import BaseModel, Field

from fastapi import APIRouter, Path, Query, Cookie, Header
from enum import Enum

from datetime import date

app03 = APIRouter()

"""Path Parameters and Number Validations 路径参数和数字验证"""


# 无参数
@app03.get('/path_params01/parameters')
async def path_params01():
    return {'message': 'This is a message'}


# 路径参数
@app03.get('/path_params02/{parameters}')
async def path_params02(parameters: str):
    return {'message': parameters}


class CityName(str, Enum):
    Beijing = 'Baijing China'
    Shanghai = 'Shanghai China'


# 枚举类型参数
@app03.get('/latest/{city}')
async def latest(city: Optional[CityName] = None):
    if city == CityName.Shanghai:
        return {'city_name': city, 'confirmed': 1492, 'death': 7}
    if city == CityName.Beijing:
        return {'city_name': city, 'confirmed': 971, 'death': 9}
    return {'city_name': city, 'latest': 'unknown'}


# 通过path parameters传递文件路径
@app03.get('/filepath/{file_path: path}')
async def filepath(file_path: str):
    return f'The file path is {file_path}'


# 路径参数校验 ...相当于None
# 路径参数用Path()类校验
@app03.get('path_params_validate/{num}')
async def path_params_validate(num: int = Path(...,
                                               ge=1,
                                               le=10,
                                               title='Your number',
                                               description='1<=num<=10')
                               ):
    return num


"""Query Parameters and String Validations 查询参数和字符串验证"""


@app03.get('query_page_limit')
async def query_page_limit(page: Optional[int] = 1, limit: Optional[int] = None):
    if limit:
        return {'page': page, 'limit': limit}
    return {'gage': page}


# 布尔类型转换
@app03.get('/query_type_conversion')
async def query_type_conversion(param: bool = False):
    return param


# 多个查询参数的列表、参数别名
# 查询参数用Query()类 校验
@app03.get('query_params_validate')
async def query_params_validate(value: str = Query(..., min_length=8, max_length=16, regex='^a'),
                                values: List[str] = Query(default=['v1', 'v2'], alias='alias_name')
                                ):
    return value, values


"""Request Body and Fields 请求体和字段"""


class CityInfo(BaseModel):
    name: str = Field(..., example='Beijing')  # example的值是注解，不会被验证
    country: str
    country_code: str = None  # 默认可以不填写
    country_population: int = Field(default=800, title='人口数量', description='国家的人口数量', ge=800)

    class Config:
        schema_extra = {
            'example': {
                'name': 'Shanghai',
                'country': 'China',
                'country_code': 'CN',
                'country_population': 140000000
            }
        }


@app03.post('/request_body/city')
async def city_info(city: CityInfo):
    print(city.name, city.country)
    return city.dict()


"""Request Body + Path parameters + Query parameters 多参数混合体"""


@app03.put('/request_body/city/{name}')
async def mix_city_info(
        name: str,  # 路径参数
        city01: CityInfo,  # 请求体Body
        city02: CityInfo,  # 请求体Body Body可以定义是多个的
        confirmed: int = Query(ge=0, description='确诊数', default=0),  # 查询参数
        death: int = Query(ge=0, description='死亡数', default=0),  # 查询参数
):
    if name == 'Shanghai':
        return {'Shanghai': {'confirmed': confirmed, 'death': death}}
    return city01.dict(), city02.dict()


"""Request Body - Nested Models 数据格式嵌套的请求体"""


class Data(BaseModel):
    city: List[CityInfo] = None  # 定义数据格式嵌套的请求体
    date: date
    confirmed: int = Field(ge=0, description='确诊数', default=0)
    deaths: int = Field(ge=0, description='死亡数', default=0)
    recovered: int = Field(ge=0, description='痊愈数', default=0)


@app03.put('/request_body/nested')
async def nested_models(data: Data):
    return data


"""Cookie 和 Header 参数"""


@app03.get('/cookie')
async def cookie(cookie_id: Optional[str] = Cookie(None)):
    return {'cookie_id': cookie_id}


@app03.get('/header')
async def cookie(user_agent: Optional[str] = Header(None, convert_underscores=True), x_token: List[str] = Header(None)):
    """
    有些HTTP代理和服务器不允许在请求头中带有下划线的，所以Header提供convert_underscores=True转换为-
    :param user_agent: user_agent 变成 user-agent
    :param x_token: 是包含多个值的表
    :return:
    """
    return {'User-Agent': user_agent, 'x_token': x_token}


