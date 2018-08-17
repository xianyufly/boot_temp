# coding: utf-8
from sqlalchemy import Column, INTEGER, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TIpPool(Base):
    __tablename__ = 't_ip_pool'

    id = Column(INTEGER(), primary_key=True)
    ip = Column(String(50))
    port = Column(String(10))
