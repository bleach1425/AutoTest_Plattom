import uvicorn
from typing import Optional
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def index():
    return "Wellcome to the Fasterapi"

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)