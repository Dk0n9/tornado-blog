# coding: utf8
"""
后台文章管理模块和撰写文章页面处理
"""

import model
from handlers import base


class AdminArticlesHandler(base.AdminHandler):

    def initialize(self, **kwargs):
        super(AdminArticlesHandler, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def get(self, *args, **kwargs):
        articleLists = self._dbOperate.getArticleLists()
        self.render('admin/articles.html', articles=articleLists)


class AdminWriteArticle(base.AdminHandler):

    def initialize(self, **kwargs):
        super(AdminWriteArticle, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def get(self, *args, **kwargs):
        self.render('admin/write.html', editMode=0)

    def post(self, *args, **kwargs):
        message = {
            'status': False,
            'message': '',
            'result': ''
        }
        info = {
            'article_title': self.get_argument('article_title', ''),
            'article_author': self.get_argument('article_author', ''),
            'article_content': self.get_argument('article_content', ''),
            'article_is_draft': self.get_argument('article_is_draft', ''),
            'article_is_hidden': self.get_argument('article_is_hidden', ''),
            'tag_name': self.get_argument('tag_name', '').split(','),
            'article_create_timestamp': self.functions.getNowTime()
        }

        isSuccess = self._dbOperate.addArticleByDict(info)
        if not isSuccess:
            message['message'] = u'新增失败'
            return self.write(message)

        message['status'] = True
        message['message'] = u'新增成功'
        self.write(message)


class AdminArticleInfo(base.AdminHandler):

    def initialize(self, **kwargs):
        super(AdminArticleInfo, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def post(self, *args, **kwargs):
        message = {
            'status': False,
            'message': '',
            'result': ''
        }

        articleID = self.get_argument('article_id', '')
        if not articleID or not articleID.isdigit():
            message['message'] = u'文章ID有误'
            return self.write(message)

        articleInfo = self._dbOperate.getArticleInfoByID(articleID)
        if not articleInfo:
            message['message'] = u'文章ID有误'
            return self.write(message)

        articleInfo = articleInfo.__dict__
        del articleInfo['_sa_instance_state']
        message['status'] = True
        message['result'] = articleInfo
        self.write(message)


class AdminArticleUpdate(base.AdminHandler):

    def initialize(self, **kwargs):
        super(AdminArticleUpdate, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def post(self, *args, **kwargs):
        message = {
            'status': False,
            'message': '',
            'result': ''
        }

        articleID = self.get_argument('article_id', '')
        articleTitle = self.get_argument('article_title', '')
        articleAuthor = self.get_argument('article_author', '')
        articleContent = self.get_argument('article_content', '')
        articleIsDraft = self.get_argument('article_is_draft', '')
        articleIsHidden = self.get_argument('article_is_hidden', '')

        isSuccess = self._dbOperate.updateArticleInfo(articleID, articleTitle, articleAuthor,
                                                      articleContent, articleIsDraft, articleIsHidden)
        if not isSuccess:
            message['message'] = u'更新失败'
            return self.write(message)

        message['status'] = True
        message['message'] = u'更新成功'
        self.write(message)


class AdminArticleDelete(base.AdminHandler):

    def initialize(self, **kwargs):
        super(AdminArticleDelete, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def post(self, *args, **kwargs):
        message = {
            'status': False,
            'message': '',
            'result': ''
        }

        articleID = self.get_argument('article_id', '')
        if not articleID or not articleID.isdigit():
            message['message'] = u'文章ID有误'
            return self.write(message)

        isSuccess = self._dbOperate.deleteArticleByID(articleID)
        if not isSuccess:
            message['message'] = u'删除失败'
            return self.write(message)

        message['status'] = True
        message['message'] = u'删除成功'
        self.write(message)