from fastapi import Depends
from strawberry.fastapi import BaseContext

from application import BooksService


class Applications:
    def __init__(self, books: BooksService):
        self.books = books


class Context(BaseContext):
    def __init__(self, applications: Applications) -> None:
        self.applications = applications


async def get_context(
    books_service: BooksService = Depends(BooksService),
) -> Context:
    applications = Applications(books=books_service)
    return Context(applications=applications)
