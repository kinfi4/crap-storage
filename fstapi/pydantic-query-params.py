from typing import Annotated

from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel


app = FastAPI()


class RowSpan(BaseModel):
    span: tuple[int, int]


@app.get("/")
async def get(query: Annotated[RowSpan, Query()]):
    print(query.span)
