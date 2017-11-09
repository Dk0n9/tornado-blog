# coding: utf-8
from tornado.web import url

from handlers.index.handler import *
from handlers.admin.index.handler import *
from handlers.admin.post.handler import *


def getRoutes(options):
    routes = []

    # <-- ADMIN MODULE --> #
    routes.extend([url(r'^/admin/login$', AdminLoginHandler, dict(options), name='adminLogin'),
                   url(r'^/admin/index$', AdminIndexHandler, dict(options), name='adminIndex')
                  ])

    # <-- ADMIN ARTICLE MODULE --> #
    routes.extend([url(r'^/admin/posts$', AdminPostsHandler, dict(options), name='adminPosts'),
                   url(r'^/admin/posts/info$', AdminPostInfo, dict(options), name='postInfo'),
                   url(r'^/admin/write$', AdminWritePost, dict(options), name='adminWrite'),
                   url(r'^/admin/posts/edit$', AdminPostEdit, dict(options), name='postEdit'),
                   url(r'^/admin/posts/delete$', AdminPostDelete, dict(options), name='postDelete'),
                   url(r'^/admin/posts/tags$', AdminPostTags, dict(options), name='postTags'),
                   ])

    # <-- INDEX MODULE --> #
    routes.extend([url(r'^/$|^/index$', IndexHandler, dict(options), name='blogIndex'),
                   url(r'^/post/\d{1,9}$', PostDetailHandler, dict(options), name='blogDetail')
                   ])

    return routes
