# coding: utf-8
from sqlalchemy import Column
from sqlalchemy.dialects.mysql.types import INTEGER, VARCHAR, CHAR

import db


class Model(db.Base):
    """程序配置表"""
    __tablename__ = 'settings'
    site_title = Column(VARCHAR(255))
    user_name = Column(VARCHAR(50))
    user_pwd = Column(CHAR(32))
    user_avatar = Column(VARCHAR(255))
    page_number = Column(INTEGER(11))
