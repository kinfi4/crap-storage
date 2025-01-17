from typing import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session


class SessionManager:
    def __init__(self, db_uri: str, isolation_level: str = "REPEATABLE READ") -> None:
        self._engine = create_engine(url=db_uri, isolation_level=isolation_level)
        self.session_factory = scoped_session(sessionmaker(bind=self._engine))

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        session = self.session_factory()

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
