from fastapi import FastAPI

from fast_api_zero.routes import auth, users
from fast_api_zero.schemas import Message

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)


@app.get('/', status_code=200, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}
