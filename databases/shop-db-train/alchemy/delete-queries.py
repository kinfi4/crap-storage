from sqlalchemy.orm import Session

from session_manager import SessionManager
from tables import User


def delete_user_by_id() -> None:
    user_id = 1

    with manager.session() as session:
        session: Session
        session.query(User).filter(User.id == user_id).delete()  # doesn't work for some reason :((
        # or
        user = session.query(User).get(user_id)
        session.delete(user)

        session.rollback()  # to cancel the delete operation


if __name__ == "__main__":
    manager = SessionManager("postgresql+psycopg2://postgres:postgres@localhost/stop_db")

    delete_user_by_id()
