"""
连接数据库
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# 初始化数据库连接:
HOST = '47.241.35.150'
PORT = '3306'
DATABASE = 'library'
USERNAME = 'root'
PASSWORD = 'Kadfgo53254G'

DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8"
# DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,
#                                                                                         password=PASSWORD,
#                                                                                         host=HOST,
#                                                                                         port=PORT,
#                                                                                         db=DATABASE)
engine = create_engine(DB_URI, echo=True, encodings='utf-8')
# 创建DBSession类型:
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)



