from fastapi import FastAPI

from fast_api_zero.schemas import Message

app = FastAPI()


@app.get('/', status_code=200, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}
