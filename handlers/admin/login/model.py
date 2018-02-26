# coding: utf8
from models.settings import Model as settingModel
from models.posts import Model as postModel


class Model(object):

    def __init__(self, dbSession):
        self._session = dbSession

    def checkUser(self, userName, userPwd):
        try:
            raw = self._session.query(settingModel).filter(settingModel.user_name == userName,
                                                           settingModel.user_pwd == userPwd).one()
            if raw:
                return True
            return False
        except Exception, e:
            return False

    def getPostCount(self):
        raw = self._session.query(postModel.id).count()
        return raw
