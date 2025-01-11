import datetime as dt

import strawberry as st
from fastapi import Depends

from database.tables import Book


@st.type
class AuthorType:
    id: int
    name: str
    age: int
    time_created: dt.datetime
    time_updated: dt.datetime


@st.type
class BookType:
    id: int
    title: str
    rating: int
    author_id: int
    author: AuthorType
    time_created: dt.datetime
    time_updated: dt.datetime


@st.type
class Query:
    @st.field(graphql_type=list[BookType])
    def all_books(self, info: st.Info) -> list[Book]:
        fields: list[str] = [field.name for field in info.selected_fields[0].selections]
        books = info.context.applications.books.load_books(fields=fields)
        return books

    @st.field
    def book(self, id: int, info: st.Info) -> BookType:
        print(info.field_name)
        books_data = info.context.applications.books.book_by_id(id)
        return BookType(**books_data.as_dict())
