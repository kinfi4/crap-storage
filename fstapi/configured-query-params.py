from typing import Annotated

from fastapi import FastAPI, Depends


app = FastAPI()


class CommonQueryParams:
    def __init__(self, q: str = None, skip: int = 0, limit: int = 100) -> None:
        self.q = q
        self.skip = skip
        self.limit = limit

    async def __call__(self, q: str, skip: int | None = None, limit: int | None = None) -> "CommonQueryParams":
        self.q = q

        if skip is not None:
            self.skip = skip
        if limit is not None:
            self.limit = limit

        return self


default_params = CommonQueryParams(skip=5, limit=5)


@app.get("/")
async def get(query: Annotated[CommonQueryParams, Depends(default_params)]):
    print(query.q, query.skip, query.limit)
