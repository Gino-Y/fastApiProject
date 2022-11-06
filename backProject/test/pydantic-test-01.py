from pydantic import BaseModel, ValidationError, constr
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base


class User(BaseModel):
    id: int  # 必填字段
    name: str = 'John Snow'
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


external_data = {
    'id': '123',
    'signup_ts': datetime.now(),
    'friends': [1, 2, '3']
}

user = User(**external_data)
# print(user.id, user.friends, user.signup_ts)
# print(user.dict())
# print(user.json())

# try:
#     User(id=1, signup_ts=datetime.today(), friends=[1, 2, 'NAN'])
# except ValidationError as e:
#     print(e.json())

print(user.dict())
print(user.json())
print('解析对象：{content}'.format(content=User.parse_obj(obj=external_data)))  # 解析对象
print('解包：{content}'.format(content=User))  # 解包

print('架构方案    ：{content}'.format(content=user.schema()))
print('架构方案json：{content}'.format(content=user.schema_json()))
print('---')


class Sound(BaseModel):
    sound: str


class Dog(BaseModel):
    birthday: date
    weight: float = Optional[None]
    sound: List[Sound]


dogs = Dog(birthday=date.today(),
           weight=6.66,
           sound=[
               {'sound': 'wang wang'},
               {'sound': 'ying ying'},
           ])

print(dogs.dict())
print('表模型---设计表---')
Base = declarative_base()


# 数据表的模型类
class CompanyOrm(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    name = Column(String(63), unique=True)
    domains = Column(ARRAY(String(255)))


# pydantic 定义好的的模型规范格式
class CompanyMode(BaseModel):
    id: int
    public_key: constr(max_length=20)
    name: constr(max_length=64)
    domains: List[constr(max_length=255)]

    class Config:
        orm_mode = True


# 数据
co_orm = CompanyOrm(
    id=123,
    public_key='foobar',
    name='Testing',
    domains=['example.com', 'imooc.com']
)

print(CompanyMode.from_orm(co_orm))
