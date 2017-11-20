# coding: utf-8
from tornado.web import url

from handlers.index.handler import *
from handlers.admin.login.handler import *
from handlers.admin.post.handler import *


def getRoutes(options):
    routes = []

    # <-- ADMIN MODULE --> #
    routes.extend([url(r'^/admin/login$', AdminLoginHandler, dict(options), name='adminLogin')  # 后台登录页面
                  ])

    # <-- ADMIN ARTICLE MODULE --> #
    routes.extend([url(r'^/admin/posts$', AdminPostsHandler, dict(options), name='adminPosts'),  # 文章列表页面
                   url(r'^/admin/posts/info$', AdminPostInfo, dict(options), name='postInfo'),
                   url(r'^/admin/write$', AdminWritePost, dict(options), name='adminWrite'),  # 编写文章页面
                   url(r'^/admin/posts/edit$', AdminPostEdit, dict(options), name='postEdit'),
                   url(r'^/admin/posts/delete$', AdminPostDelete, dict(options), name='postDelete'),
                   url(r'^/admin/posts/tags$', AdminPostTags, dict(options), name='postTags'),
                   ])

    # <-- INDEX MODULE --> #
    routes.extend([url(r'^/$|^/index$', IndexHandler, dict(options), name='blogIndex'),  # 博客首页
                   url(r'^/post/\d{1,9}$', PostDetailHandler, dict(options), name='blogDetail')  # 文章详情页面
                   ])

    # <-- INSTALL MODULE --> #
    routes.extend([url(r'^/install$', InstallHandler, dict(options), name='blogInstall'),  # 安装页面
                   ])

    return routes
