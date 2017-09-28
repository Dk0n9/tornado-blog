# coding: utf-8
from tornado.web import url

from handlers.admin.index.handler import *
from handlers.admin.article.handler import *


def getRoutes(options):
    routes = []

    # <-- ADMIN MODULE --> #
    routes.extend([url(r'^/admin/login.asp$', AdminLoginHandler, dict(options), name='adminLogin'),
                   url(r'^/admin/index.asp$', AdminIndexHandler, dict(options), name='adminIndex')
                  ])

    # <-- ARTICLE MODULE --> #
    routes.extend([url(r'^/admin/write.asp$', AdminWriteArticle, dict(options), name='adminWrite')
                   ])

    return routes
