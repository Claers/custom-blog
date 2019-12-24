"""Models for blog app
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey, Boolean, Table
from sqlalchemy_utils import URLType
from sqlalchemy.orm import sessionmaker, relationship
from .settings import DB_NAME, DB_PASSWORD, DB_USER, DB_HOST

def get_url():
    return "postgresql+psycopg2://%s:%s@%s/%s" % (
        DB_USER,
        DB_PASSWORD,
        DB_HOST,
        DB_NAME,
    )


Base = declarative_base()
engine = create_engine(get_url())
Session = sessionmaker(engine)
session = Session()


class Article(Base):
    """Simple article model
    """

    __tablename__ = "article"
    id = Column(Integer, primary_key=True)
    name = Column(String)


Base.metadata.create_all(engine)
