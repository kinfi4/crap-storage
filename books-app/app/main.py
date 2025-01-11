import uvicorn
from fastapi import FastAPI

from api.rest import router as rest_router
from api.graphql import router as graphql_router

app = FastAPI()

app.include_router(rest_router)
app.include_router(graphql_router, prefix="/graphql")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
