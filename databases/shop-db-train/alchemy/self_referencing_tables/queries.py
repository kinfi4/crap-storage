from typing import Iterable

from sqlalchemy.orm import Session

from alchemy.session_manager import SessionManager
from alchemy.self_referencing_tables.table import Comment


if __name__ == "__main__":
    manager = SessionManager("postgresql+psycopg2://postgres:postgres@localhost/shop_db")

    with manager.session() as session:
        session: Session

        # root_comment = Comment(id=1, text="Hello, world")
        # sub_root1 = Comment(text="Hello, dude!", parent_id=root_comment.id)
        # sub_root2 = Comment(text="Hello!", parent_id=sub_root1.id)
        # #
        # session.bulk_save_objects([root_comment, sub_root1, sub_root2])
        # session.commit()

        results: Iterable[Comment] = session.query(Comment).where(Comment.parent_id.isnot(None))

        for comment in results:
            print(comment.text, comment.parent.text, comment.parent_id)
