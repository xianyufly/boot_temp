# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class WyCookie(Base):
    __tablename__ = 'wy_cookie'

    account_str = Column(String(50), primary_key=True)
    web_wx_rc = Column(String(255))
    pgv_pvi = Column(String(255))
    pgv_si = Column(String(255))
    ptisp = Column(String(255))
    ptui_loginuin = Column(String(255))
    pt2gguin = Column(String(255))
    uin = Column(String(255))
    skey = Column(String(255))
    ptcz = Column(String(255))
    p_uin = Column(String(255))
    pt4_token = Column(String(255))
    p_skey = Column(String(255))
    wyctoken = Column(String(255))
    rootDirKey = Column(String(255))
    mainDirKey = Column(String(255))
