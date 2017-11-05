# coding: utf-8
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql.types import INTEGER, VARCHAR

import db


class Model(db.Base):
    """一对多关系表，文章 > 多个标签"""
    __tablename__ = 'tbl_post_tags'
    post_tags_id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    tbl_posts_post_id = Column(INTEGER(11))
    tbl_tags_tag_id = Column(INTEGER(11))
