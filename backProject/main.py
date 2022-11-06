import uvicorn
from fastapi import FastAPI

from test import app03
from test import app04
from test import app05
from test import app06
from test import app07
from test import app08

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='127.0.0.1', port=8000, reload=True, workers=1)


