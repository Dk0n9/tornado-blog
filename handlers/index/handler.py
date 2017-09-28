# coding: utf8
"""
首页模块
"""

import model
from handlers import base


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

        articleLists = self._dbOperate.getArticlesList(bool(self.current_user),
                                                       num=self.current_user.setting_page_number, page=page)

