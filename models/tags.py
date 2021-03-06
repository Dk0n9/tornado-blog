# coding: utf-8
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql.types import INTEGER, VARCHAR

import db


class Model(db.Base):
    """文章标签表"""
    __tablename__ = 'tags'
    tag_name = Column(VARCHAR(100), index=True)
    quoteNumber = Column(INTEGER(11), default=0)  # 标签引用次数
