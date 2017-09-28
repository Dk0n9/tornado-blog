# coding: utf8
from models.articles import Model as articleModel
from models.article_tags import Model as articleTagsModel
from models.tags import Model as tagModel
from models import db


class Model(object):

    def __init__(self, dbSession):
        self._session = dbSession

    def getArticlesList(self, isUser, num=10, page=1):
        """用于前台获取文章列表，isUser是根据当前用户的状态来决定是否显示已设置为隐藏状态的文章"""
        info = {
            'total': '',
            'result': {}
        }
        startOffset = page * num - num
        query = self._session.query(articleModel).filter(articleModel.article_draft == 0)
        if not isUser:
            query = query.filter(articleModel.article_hidden == 1)
        info['total'] = query.count()
        raw = query.order_by(db.DESC(articleModel.article_create_timestamp)).offset(startOffset).limit(num).all()
        for record in raw:
            info['result'][record.id] = {
                'author': record.article_author,
                'title': record.article_title,
                'content': record.article_content,
                'browser': record.article_browser,
                'timestamp': record.article_create_timestamp,
                'tags': []
            }
            tagList = self._getTagsByArticleID(record.id)
            info['result'][record.id]['tags'] = tagList
        return info

    def _getTagsByArticleID(self, articleID):
        result = []
        raw = self._session.query(tagModel).join(articleTagsModel).\
            filter(articleTagsModel.tbl_articles_article_id == articleID).all()
        for tag in raw:
            result.append(tag.tag_name)
        return result
