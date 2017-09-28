# coding: utf8
from models.settings import Model as settingModel
from models.articles import Model as articleModel


class Model(object):

    def __init__(self, dbSession):
        self._session = dbSession

    def checkUser(self, userName, userPwd):
        try:
            raw = self._session.query(settingModel).filter(settingModel.setting_user_name == userName,
                                                           settingModel.setting_user_pwd == userPwd).one()
            if raw:
                return True
            return False
        except Exception, e:
            return False

    def getArticleCount(self):
        raw = self._session.query(articleModel.article_id).count()
        return raw
