from typing import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session


class SessionManager:
    def __init__(self, db_uri: str) -> None:
        self._engine = create_engine(url=db_uri)
        self.Session = scoped_session(sessionmaker(bind=self._engine))

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        session = self.Session()

        try:
            yield session
            session.commit()
        except Exception as e:
            print("The query failed with error:", str(e))
            session.rollback()
            # Custom logging or error handling here
            raise e
        finally:
            session.close()
