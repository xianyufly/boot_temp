# coding: utf-8
from sqlalchemy import Column, INTEGER, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class WyQq(Base):
    __tablename__ = 'wy_qq'
    tid = Column(INTEGER(), primary_key=True)
    account_str = Column(String(50))
    pwd_str = Column(String(50))
    is_can_upload = Column(INTEGER(), server_default=text("'0'"))
