import os
import contextlib
from typing import Generator

from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy import create_engine

engine = create_engine(os.environ.get("DATABASE_URL"), echo=True)
session_factory = scoped_session(sessionmaker(bind=engine))


def session_maker() -> Session:
    s = session_factory()
    s.begin()
    try:
        yield s
        print("Committing The Session")
        s.commit()
    except:
        s.rollback()
    finally:
        print("Closing The Session")
        s.close()
