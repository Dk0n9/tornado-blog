# coding: utf-8
from sqlalchemy import Column
from sqlalchemy.dialects.mysql.types import INTEGER, VARCHAR, CHAR

import db


class Model(db.Base):
    """程序配置表"""
    __tablename__ = 'tbl_settings'
    setting_id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    setting_site_title = Column(VARCHAR(255))
    setting_user_name = Column(VARCHAR(50))
    setting_user_pwd = Column(CHAR(32))
    setting_user_avatar = Column(VARCHAR(255))
    setting_page_number = Column(INTEGER(11))
