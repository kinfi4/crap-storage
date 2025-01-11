from fastapi import APIRouter, Depends

from api.rest.serializers import SerializedBook, SerializedAuthor, CreateBookRequest, CreateAuthorRequest
from application import BooksService

router = APIRouter(prefix="/api")


@router.post("/books", response_model=SerializedBook)
def add_book(
    book: CreateBookRequest,
    app: BooksService = Depends(BooksService),
):
    created_book = app.add_book(
        title=book.title,
        rating=book.rating,
        author_id=book.author_id,
    )

    return SerializedBook.model_validate(created_book)


@router.post("/authors", response_model=SerializedAuthor)
def add_author(
    author: CreateAuthorRequest,
    app: BooksService = Depends(BooksService)
):
    created_author = app.add_author(
        name=author.name,
        age=author.age,
    )

    return SerializedAuthor.model_validate(created_author)


@router.get("/books", response_model=list[SerializedBook])
def get_books(app: BooksService = Depends(BooksService)):
    return app.load_books()
