# coding: utf-8
from os.path import dirname, isfile

from tornado.web import RequestHandler

from models.settings import Model as SettingModel


class BaseHandler(RequestHandler):

    db = None
    functions = None
    logging = None

    def initialize(self, **kwargs):
        if kwargs:
            self.db = kwargs.get('db')
            self.functions = kwargs.get('functions')
            self.logging = kwargs.get('logging')
            self.siteTitle = self.db.query(SettingModel.setting_site_title).first()[0]

    def prepare(self):
        if self.isInstalled:
            pass
        else:
            return self.redirect(self.reverse_url('blogInstall'))

    @property
    def isInstalled(self):
        currentPath = dirname(__file__)
        return isfile(currentPath + '/../install.lck')

    @property
    def getUserIP(self):
        return self.request.remote_ip

    @property
    def getSetting(self):
        try:
            raw = self.db.query(SettingModel).first()
            return raw
        except Exception, e:
            return False

    def get_login_url(self):
        return self.reverse_url('login')

    def get_current_user(self):
        userName = self.get_secure_cookie('session', None)
        if userName is None:
            return None
        try:
            raw = self.db.query(SettingModel).filter(SettingModel.setting_user_name==userName).one()
            return raw
        except Exception, e:
            return False

    def get_template_namespace(self):
        """
        update namespace
        """
        namespace = super(BaseHandler, self).get_template_namespace()
        name = {
            'sftime': self.functions.formatTime,
            'siteTitle': self.siteTitle
        }
        namespace.update(name)
        return namespace

    def on_finish(self):
        self.db.close()

    def write_error(self, status_code, **kwargs):
        # 405状态码转404
        if status_code == 405:
            status_code = 404
        self.set_status(200)
        self.render('error.html', error=status_code)


class AdminHandler(BaseHandler):

    def initialize(self, **kwargs):
        super(AdminHandler, self).initialize(**kwargs)

    def prepare(self):
        if not self.current_user:
            return self.redirect(self.reverse_url('adminLogin'))
