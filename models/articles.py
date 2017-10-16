# coding: utf-8
from sqlalchemy import Column
from sqlalchemy.dialects.mysql.types import INTEGER, VARCHAR, TINYINT, TEXT

import db


class Model(db.Base):
    """文章表"""
    __tablename__ = 'tbl_articles'
    article_id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    article_author = Column(VARCHAR(100))  # 显示的作者名称
    article_title = Column(VARCHAR(100))
    article_content = Column(TEXT())
    article_is_draft = Column(TINYINT(1))  # 设置文章是否为草稿；1：是；0：否；如果为草稿，则不显示在首页文章列表中
    article_is_hidden = Column(TINYINT(1))  # 设置文章可见性；1：所有人可见；0：仅自己可见
    article_browser = Column(INTEGER(11), default=0)  # 文章浏览数量
    article_create_timestamp = Column(INTEGER(11))