# coding: utf-8
from sqlalchemy import Column, INTEGER, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TSubject(Base):
    __tablename__ = 't_subject'

    tid = Column(INTEGER(), primary_key=True)
    sub_code = Column(String(20))
    sub_name = Column(String(20))
    sub_status = Column(INTEGER(), server_default=text("'0'"))
