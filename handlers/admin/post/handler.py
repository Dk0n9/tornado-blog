# coding: utf8
"""
后台文章管理模块和撰写文章页面处理
"""

import model
from handlers import base


class AdminPostsHandler(base.AdminHandler):

    def initialize(self, **kwargs):
        super(AdminPostsHandler, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def get(self, *args, **kwargs):
        postLists = self._dbOperate.getPostLists()
        self.render('admin/posts.html', postLists=postLists)


class AdminWritePost(base.AdminHandler):

    def initialize(self, **kwargs):
        super(AdminWritePost, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def get(self, *args, **kwargs):
        self.render('admin/write.html', editMode=0)

    def post(self, *args, **kwargs):
        message = {
            'status': False,
            'message': '',
            'result': ''
        }
        info = {
            'post_title': self.get_argument('post_title', '').encode('utf8'),
            'post_author': self.get_argument('post_author', ''),
            'post_summary': self.get_argument('post_summary', ''),
            'post_content': self.get_argument('post_content', ''),
            'post_is_draft': self.get_argument('post_is_draft', ''),
            'post_is_hidden': self.get_argument('post_is_hidden', ''),
            'tag_name': self.get_argument('tag_name', '').split(','),
            'post_create_timestamp': self.functions.getNowTime()
        }

        isSuccess = self._dbOperate.addPostByDict(info)
        if not isSuccess:
            message['message'] = u'发布失败'
            return self.write(message)

        message['status'] = True
        message['message'] = u'发布成功，即将跳转至文章管理页面...'
        message['result'] = self.reverse_url('adminPosts')
        self.write(message)


class AdminPostInfo(base.AdminHandler):

    def initialize(self, **kwargs):
        super(AdminPostInfo, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def post(self, *args, **kwargs):
        message = {
            'status': False,
            'message': '',
            'result': ''
        }

        postID = self.get_argument('post_id', '')
        if not postID or not postID.isdigit():
            message['message'] = u'文章ID有误'
            return self.write(message)

        info = self._dbOperate.getPostInfoByID(postID)
        if not info:
            message['message'] = u'文章ID有误'
            return self.write(message)

        postInfo = info['post'].__dict__
        del postInfo['_sa_instance_state']
        message['status'] = True
        message['result'] = postInfo
        self.write(message)


class AdminPostEdit(base.AdminHandler):

    def initialize(self, **kwargs):
        super(AdminPostEdit, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def get(self, *args, **kwargs):
        postID = self.get_query_argument('id', '')
        info = self._dbOperate.getPostInfoByID(postID)
        if not info:
            return self.write_error(404)
        self.render('admin/write.html', postInfo=info['post'], tags=info['tags'], editMode=1)

    def post(self, *args, **kwargs):
        message = {
            'status': False,
            'message': '',
            'result': ''
        }

        postID = self.get_argument('post_id', '')
        postTitle = self.get_argument('post_title', '')
        postAuthor = self.get_argument('post_author', '')
        postSummary = self.get_argument('post_summary', '')
        postContent = self.get_argument('post_content', '')
        postIsDraft = self.get_argument('post_is_draft', '')
        postIsHidden = self.get_argument('post_is_hidden', '')
        postTags = self.get_argument('tag_name', '').split(',')

        isSuccess = self._dbOperate.updatePostInfo(postID, postTitle, postAuthor, postSummary,
                                                      postContent, postIsDraft, postIsHidden, postTags)
        if not isSuccess:
            message['message'] = u'更新失败'
            return self.write(message)

        message['status'] = True
        message['message'] = u'更新成功'
        self.write(message)


class AdminPostDelete(base.AdminHandler):

    def initialize(self, **kwargs):
        super(AdminPostDelete, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def post(self, *args, **kwargs):
        message = {
            'status': False,
            'message': '',
            'result': ''
        }

        postID = self.get_argument('post_id', '')
        if not postID or not postID.isdigit():
            message['message'] = u'文章ID有误'
            return self.write(message)

        isSuccess = self._dbOperate.deletePostByID(postID)
        if not isSuccess:
            message['message'] = u'删除失败'
            return self.write(message)

        message['status'] = True
        message['message'] = u'删除成功'
        self.write(message)


class AdminPostTags(base.AdminHandler):

    def initialize(self, **kwargs):
        super(AdminPostTags, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def post(self, *args, **kwargs):
        message = {
            'status': True,
            'message': '',
            'result': ''
        }

        postID = self.get_argument('postID', '')
        if not postID:
            tags = self._dbOperate.getAllTags()
            message['result'] = tags
            self.write(message)
            return self.finish()
        if not postID.isdigit():
            message['status'] = False
            message['message'] = u'文章ID有误'
            self.write(message)
            return self.finish()
        data = self._dbOperate.getTagsByPostID(postID)
        message['result'] = data
        self.write(message)
