"""Models for blog app
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey, Boolean, Table, LargeBinary
from sqlalchemy_utils import URLType
from sqlalchemy.orm import sessionmaker, relationship
from settings import DB_NAME, DB_PASSWORD, DB_USER, DB_HOST


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
    content = Column(String)
    description = Column(String)
    desc_img = Column(LargeBinary)
    desc_img_url = Column(URLType)
    img = Column(LargeBinary)
    img_url = Column(URLType)
    pinned = Column(Boolean)
    categories = Column(String)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content
        }


class GameArticle(Base):
    """A game article model

    Arguments:
        Article {[type]} -- [description]
    """
    __tablename__ = "game_article"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    content = Column(String)
    desc_img = Column(LargeBinary)
    img = Column(LargeBinary)
    game_url = Column(URLType)


