# coding: utf-8
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import asc, desc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql.types import INTEGER
from sqlalchemy.ext.declarative import declarative_base, declared_attr

__all__ = ['Base', 'init', 'ASC', 'DESC']

ASC = asc
DESC = desc


class Base(declarative_base()):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return 'tbl_' + cls.__name__

    @classmethod
    def __table_cls__(cls, name, metadata, *arg, **kw):
        return Table(
            "tbl_" + name,
            metadata, *arg, **kw
        )

    id = Column(INTEGER, primary_key=True, autoincrement=True)


def init(settings):
    engine = create_engine('{0}://{1}:{2}@{3}:{4}/{5}?charset={6}'.format(settings['driver'], settings['user'],
                                                                          settings['pass'], settings['host'],
                                                                          settings['port'], settings['db'],
                                                                          settings['charset']),
                           encoding=settings['charset'], echo=settings.get('debug', False))
    engine.recycle = 3600
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    session.execute('SET NAMES {0}'.format(settings['charset']))  # 解决在部分机器上的编码问题
    return session
