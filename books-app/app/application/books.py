from typing import Type

from fastapi import Depends
from sqlalchemy.orm import Session, joinedload, load_only

from database import session_maker, Book, Author


class BooksService:
    def __init__(self, session: Session = Depends(session_maker)) -> None:
        self.session = session

    def load_books(self, fields: list[str] = None) -> list[Type[Book]]:
        query = self.session.query(Book).options(joinedload(Book.author))

        if fields is not None:
            print(Book.aliases_to_columns(fields))
            query = query.options(load_only(*Book.aliases_to_columns(fields)))

        return query.all()

    def book_by_id(self, id: int, fields: list[str] = None) -> Book:
        query = self.session.query(Book)

        if fields is not None:
            query = query.options(load_only(*Book.aliases_to_columns(fields)))

        return query.get({"id": id})

    def add_book(self, title: str, rating: int, author_id: int) -> Book:
        book = Book(title=title, rating=rating, author_id=author_id)

        self.session.add(book)
        self.session.commit()

        return book

    def add_author(self, name: str, age: int) -> Author:
        author = Author(name=name, age=age)

        self.session.add(author)
        self.session.commit()

        return author
