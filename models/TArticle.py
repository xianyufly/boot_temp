# coding: utf-8
from sqlalchemy import Column,DateTime, INTEGER, String, Text, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TArticle(Base):
    __tablename__ = 't_article'

    tid = Column(INTEGER(), primary_key=True)
    art_type = Column(String(20))
    title = Column(String(255))
    memo = Column(String(255))
    content = Column(Text)
    source_url = Column(String(255))
    small_pic = Column(String(255))
    source = Column(String(20))
    pub_date = Column(DateTime)
    status = Column(INTEGER(), server_default=text("'0'"))
    dir_key = Column(String(50))
    p_dir_key = Column(String(50))
    dir_name = Column(String(50), unique=True)
    qq = Column(String(50))