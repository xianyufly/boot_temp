# coding: utf-8
from sqlalchemy import Column, INTEGER, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TBootstrapRes(Base):
    __tablename__ = 't_bootstrap_res'

    tid = Column(INTEGER(), primary_key=True)
    title = Column(String(100))
    memo = Column(String(500))
    code = Column(String(20))
    face_url = Column(String(500))
    view_url = Column(String(255))
    dir_key = Column(String(50))
    p_dir_key = Column(String(50))
    dir_name = Column(String(50))
    qq = Column(String(50))
    status = Column(INTEGER(), server_default=text("'0'"))
    download_num = Column(INTEGER(), server_default=text("'0'"))
    view_num = Column(INTEGER(), server_default=text("'0'"))
    file_id = Column(String(50))