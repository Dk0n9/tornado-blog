# coding: utf8
"""
首页模块
"""

import model
from handlers import base


class InstallHandler(base.BaseHandler):

    def initialize(self, **kwargs):
        super(InstallHandler, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def get(self, *args, **kwargs):
        if self.isInstalled:
            return self.write_error(404)
        self.render('common/install.html')


class IndexHandler(base.BaseHandler):

    def initialize(self, **kwargs):
        super(IndexHandler, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def get(self, *args, **kwargs):
        page = self.get_query_argument('page', '1')
        if not page or not page.isdigit():
            page = 1
        else:
            page = int(page)

        result = self._dbOperate.getPostsList(bool(self.current_user),
                                                       num=self.getSetting.setting_page_number, page=page)
        self.render('templates/login.html', postsList=result['result'])


class PostDetailHandler(base.BaseHandler):

    def initialize(self, **kwargs):
        super(PostDetailHandler, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def get(self, *args, **kwargs):
        postID = self.request.path.split('/')[-1]
        info = self._dbOperate.getPostInfoByID(postID)
        if not info:
            self.write_error(404)
            return None
        if info['post'].post_is_hidden:
            if not self.current_user:  # 无权限查看隐藏文章将返回404页面
                self.write_error(404)
                return None
        self.render('templates/post.html', postInfo=info['post'], tags=info['tags'])
