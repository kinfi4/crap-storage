import threading
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def get():
    print(threading.currentThread().getName())  # MainThread
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def get(item_id: int):
    print(threading.currentThread().getName())  # MainThread
    return {"item_id": item_id}


@app.get("/users/me")
def read_current_user():
    print(threading.currentThread().getName())  # AnyIO worker thread
    return {"user_id": "the current user"}
