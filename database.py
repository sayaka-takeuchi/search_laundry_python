from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config

settings = config.get_settings()

engine = create_engine(url=settings.sqlalchemy_database_url, echo=True)

SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
