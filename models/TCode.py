# coding: utf-8
from sqlalchemy import Column, INTEGER, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TCode(Base):
    __tablename__ = 't_code'

    tid = Column(INTEGER(), primary_key=True)
    code = Column(String(50))
    code_desc = Column(String(50))
    code_val = Column(String(50))
