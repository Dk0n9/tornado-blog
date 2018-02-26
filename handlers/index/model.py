# coding: utf8
"""
首页数据操作模块
涉及到创建表等操作，该模块需要将 models目录中的所有 Model导入
"""

from models.posts import Model as postModel
from models.post_tags import Model as postTagsModel
from models.tags import Model as tagModel
from models import db


class Model(object):
    def __init__(self, dbSession):
        self._session = dbSession

    def getPostsList(self, isUser, num=10, page=1):
        """用于前台获取文章列表，isUser是根据当前用户的状态来决定是否显示已设置为隐藏状态的文章"""
        info = {
            'total': '',
            'result': []
        }
        startOffset = page * num - num
        query = self._session.query(postModel).filter(postModel.is_draft == 0)
        if not isUser:
            query = query.filter(postModel.is_hidden == 0)
        try:
            info['total'] = query.count()
        except Exception:
            return info
        raw = query.order_by(db.DESC(postModel.create_timestamp)).offset(startOffset).limit(num).all()
        for record in raw:
            tempRecord = {
                'id': record.id,
                'author': record.author,
                'title': record.title,
                'summary': record.summary,
                'content': record.content,
                'browser': record.browser,
                'timestamp': record.create_timestamp,
                'tags': []
            }
            tagList = self._getTagsByPostID(record.id)
            tempRecord['tags'] = tagList
            info['result'].append(tempRecord)
        return info

    def getPostInfoByID(self, postID):
        try:
            raw = self._session.query(postModel).filter(postModel.id == postID).one()
            tagList = self._getTagsByPostID(postID)
            return {
                'post': raw,
                'tags': tagList
            }
        except Exception, e:
            return False

    def _getTagsByPostID(self, postID):
        result = []
        raw = self._session.query(tagModel).join(postTagsModel, tagModel.id == postTagsModel.tag_id). \
            filter(postTagsModel.post_id == postID).all()
        for tag in raw:
            result.append(tag.tag_name)
        return result
