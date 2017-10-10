# coding: utf8
"""
后台首页，包含后台登录页的处理；
"""

import model
from handlers import base


class AdminLoginHandler(base.BaseHandler):

    def initialize(self, **kwargs):
        super(AdminLoginHandler, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def get(self, *args, **kwargs):
        if not self.current_user:
            self.render('admin/login.html')
        else:
            self.redirect(self.reverse_url('adminIndex'))

    def post(self, *args, **kwargs):
        name = self.get_argument('user_name', '')
        pwd = self.get_argument('user_pwd', '')

        message = {
            'status': False,
            'message': '',
            'result': ''
        }

        isUser = self._dbOperate.checkUser(name, pwd)
        if isUser:
            self.set_secure_cookie('session', name, expires_days=None)
            message['status'] = True
            message['message'] = u'登录成功，正在跳转...'
            message['result'] = self.reverse_url('adminIndex')
        else:
            message['message'] = u'用户名或密码不正确'
        return self.write(message)


class AdminIndexHandler(base.AdminHandler):

    def initialize(self, **kwargs):
        super(AdminIndexHandler, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def get(self, *args, **kwargs):
        articleCount = self._dbOperate.getArticleCount()
        self.render('admin/index.html', articleCount=articleCount)