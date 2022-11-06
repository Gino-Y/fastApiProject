import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class CityBase(BaseModel):
    province: str
    country: str
    is_affected: Optional[bool] = None


class CityInfo(CityBase):
    pass


class CityInclude(CityInfo):
    city: Optional[str] = None


@app.get('/')
async def hello_world():
    return {'hello': 'world'}


@app.get('/get_city/{city}')
async def get_city(city: str, quer_string: Optional[str] = None):
    return {'city': city, 'query_string': quer_string}


@app.put('/put_city/{city}')
async def put_city(city: str, city_infor: CityInfo):
    return {'city': city, 'country': city_infor.country, 'is_affected': city_infor.is_affected}


@app.put('/put_city_q')
async def put_city_q(city_infor: CityInclude):
    return {'city': city_infor.city, 'country': city_infor.country, 'is_affected': city_infor.is_affected}


# 启动命令：uvicorn hello_world:app --reload
if __name__ == '__main__':
    uvicorn.run(app='fastapi-request-verify-test:app', host='127.0.0.1', port=8031, reload=True)
