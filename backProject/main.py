import uvicorn
from fastapi import FastAPI

from test import app03, app04, app05, app06, app07, app08

app = FastAPI()

app.include_router(app03, prefix='/chapter03', tags=['第三章 请求参数和验证'])
app.include_router(app04, prefix='/chapter04', tags=['第四章 响应处理和FastAPI配置'])
app.include_router(app05, prefix='/chapter05', tags=['第五章 FastAPI的依赖注入系统'])
app.include_router(app06, prefix='/chapter06', tags=['第六章 请求参数和验证'])
app.include_router(app07, prefix='/chapter07', tags=['第七章 请求参数和验证'])
app.include_router(app08, prefix='/chapter08', tags=['第八章 临时练习'])

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='127.0.0.1', port=8000, reload=True, workers=1)


