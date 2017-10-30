# coding: utf-8
from tornado.web import url

from handlers.admin.index.handler import *
from handlers.admin.article.handler import *


def getRoutes(options):
    routes = []

    # <-- ADMIN MODULE --> #
    routes.extend([url(r'^/admin/login$', AdminLoginHandler, dict(options), name='adminLogin'),
                   url(r'^/admin/index$', AdminIndexHandler, dict(options), name='adminIndex')
                  ])

    # <-- ADMIN ARTICLE MODULE --> #
    routes.extend([url(r'^/admin/articles$', AdminArticlesHandler, dict(options), name='adminArticles'),
                   url(r'^/admin/articles/info$', AdminArticleInfo, dict(options), name='articleInfo'),
                   url(r'^/admin/write$', AdminWriteArticle, dict(options), name='adminWrite'),
                   url(r'^/admin/articles/edit$', AdminArticleEdit, dict(options), name='articleEdit'),
                   ])

    return routes
