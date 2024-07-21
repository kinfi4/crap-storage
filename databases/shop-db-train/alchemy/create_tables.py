from sqlalchemy import create_engine

from tables import Base


engine = create_engine(url="postgresql+psycopg2://postgres:postgres@localhost/alchemy_train")
Base.metadata.create_all(engine)
