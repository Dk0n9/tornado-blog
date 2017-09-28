# coding: utf8
from models.tags import Model as tagModel
from models.articles import Model as articleModel
from models.article_tags import Model as articleTagsModel


class Model(object):

    def __init__(self, dbSession):
        self._session = dbSession

    def getArticleLists(self):
        raw = self._session.query(articleModel).all()
        return raw

    def getArticleInfoByID(self, articleID):
        try:
            raw = self._session.query(articleModel).filter(articleModel.article_id==articleID).one()
            return raw
        except Exception, e:
            return False

    def updateArticleInfo(self, articleID, title, author, content, isDraft, isHidden):
        """更新文章信息"""
        articleInfo = self.getArticleInfoByID(articleID)
        if not articleInfo:
            return False

        articleInfo.article_title = title
        if articleInfo.article_author != author:
            articleInfo.article_author = author
        articleInfo.article_content = content
        if isDraft and isDraft != '0':
            articleInfo.article_draft = 1
        else:
            articleInfo.article_draft = 0
        if isHidden and isHidden != '0':
            articleInfo.article_hidden = 1
        else:
            articleInfo.article_hidden = 0

        try:
            self._session.commit()
            return True
        except Exception, e:
            self._session.rollback()
            return False

    def addArticleByDict(self, info):
        """添加文章"""
        # 调整数据格式
        if info['article_is_draft'] and info['article_is_draft'] != '0':
            info['article_is_draft'] = 1
        else:
            info['article_is_draft'] = 0
        if info['article_is_hidden'] and info['article_is_hidden'] != '0':
            info['article_is_hidden'] = 1
        else:
            info['article_is_hidden'] = 0
        # 把文章标签写入tbl_tags表中
        tagIDsList = self.addTagByList(info.pop('tag_name'))

        # 文章内容写入tbl_articles表中
        articleRecord = articleModel(**info)
        try:
            self._session.add(articleRecord)
            self._session.commit()
        except Exception, e:
            self._session.rollback()
            return False

        # 在tbl_article_tags表中添加文章与标签的关联
        for tagID in tagIDsList:
            record = articleTagsModel(tbl_articles_article_id=articleRecord.article_id, tbl_tags_tag_id=tagID)
            try:
                self._session.add(record)
            except Exception, e:
                continue
        self._session.commit()
        return True

    def deleteArticleByID(self, articleID):
        """根据文章ID删除文章"""
        articleInfo = self.getArticleInfoByID(articleID)
        if not articleInfo:
            return False

        try:
            self._session.delete(articleInfo)
            self._session.commit()
            return True
        except Exception, e:
            self._session.rollback()
            return False

    def addTagByList(self, tagsList):
        """根据输入的标签列表循环添加标签到标签表中"""
        result = []
        for tag in tagsList:
            record = tagModel(tag_name=tag)
            try:
                self._session.add(record)
                self._session.flush()
                result.append(record.id)
            except Exception, e:
                continue
        self._session.commit()
        return result
