# coding: utf-8
from sqlalchemy import Column
from sqlalchemy.dialects.mysql.types import INTEGER

import db


class Model(db.Base):
    """一对多关系表，文章 > 多个标签"""
    __tablename__ = 'post_tags'
    post_id = Column(INTEGER(11), index=True)
    tag_id = Column(INTEGER(11), index=True)
