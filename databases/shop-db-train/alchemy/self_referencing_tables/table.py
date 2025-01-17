from sqlalchemy import Text, ForeignKey, create_engine
from sqlalchemy.orm import mapped_column, MappedColumn, relationship, backref

from alchemy.tables import Base


class Comment(Base):
    __tablename__ = "comment"

    id: MappedColumn[int] = mapped_column(autoincrement=True, primary_key=True)
    text: MappedColumn[str] = mapped_column(Text(), nullable=False)

    parent_id: MappedColumn[int] = mapped_column(ForeignKey("comment.id"), nullable=True)

    children: MappedColumn[list["Comment"]] = relationship(
        "Comment",
        backref=backref('parent', remote_side=[id]),
    )


if __name__ == "__main__":
    engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost/shop_db")

    Base.metadata.create_all(engine)
