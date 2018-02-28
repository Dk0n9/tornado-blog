# coding: utf8
"""
后台文章管理模块和撰写文章页面处理
"""
import time

import model
from handlers import base


class AdminPostsHandler(base.AdminHandler):

    def initialize(self, **kwargs):
        super(AdminPostsHandler, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def get(self, *args, **kwargs):
        postLists = self._dbOperate.getPostLists()
        self.render('admin/posts.html', title='文章列表', postLists=postLists)


class AdminWritePost(base.AdminHandler):

    def initialize(self, **kwargs):
        super(AdminWritePost, self).initialize(**kwargs)
        self._dbOperate = model.Model(self.db)

    def get(self, *args, **kwargs):
        self.render('admin/write.html', title='撰写文章', editMode=0)

    def post(self, *args, **kwargs):
        message = {
            'status': False,
            'message': '',
            'result': ''
        }
        info = {
            'title': self.get_argument('postTitle', '').encode('utf8'),
            'author': self.get_argument('postAuthor', ''),
            'summary': self.get_argument('postSummary', ''),
            'content': self.get_argument('postContent', ''),
            'is_draft': self.get_argument('postIsDraft', ''),
            'is_hidden': self.get_argument('postIsHidden', ''),
            'tag_name': self.get_argument('tagName', ''),
            'create_timestamp': self.get_argument('postCreateTime', '')  # self.functions.getNowTime()
        }
        if info['tag_name']:
            info['tag_name'] = info['tag_name'].split(',')  # 避免出现长度为1的无用list
        # 转换文章发布日期的格式
        try:
            info['create_timestamp'] = time.mktime(time.strptime(info['create_timestamp'], '%Y/%m/%d %H:%M'))
        except Exception, e:
            message['message'] = u'参数错误'
            return self.write(message)

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

        postID = self.get_argument('postID', '')
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
        title = u'编辑文章' + info['post'].title
        self.render('admin/write.html', title=title, postInfo=info['post'], tags=info['tags'], editMode=1)

    def post(self, *args, **kwargs):
        message = {
            'status': False,
            'message': '',
            'result': ''
        }

        postID = self.get_argument('postID', '')
        postTitle = self.get_argument('postTitle', '')
        postAuthor = self.get_argument('postAuthor', '')
        postSummary = self.get_argument('postSummary', '')
        postContent = self.get_argument('postContent', '')
        postIsDraft = self.get_argument('postIsDraft', '')
        postIsHidden = self.get_argument('postIsHidden', '')
        postTags = self.get_argument('tagName', '').split(',')
        # 修改postCreateTime暂未实现

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

        postID = self.get_argument('postID', '')
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
            tags = self._dbOperate.getAllTags()  # tags的格式: [tag, ...]，tag的类型为model
            # 这里转换成前端chip组件autocompleteOptions参数需要的数据格式: { tag_name: null, ...}
            tempRes = {}
            for tag in tags:
                tempRes[tag.tag_name] = None
            message['result'] = tempRes
            self.write(message)
            return None
        if not postID.isdigit():
            message['status'] = False
            message['message'] = u'文章ID有误'
            self.write(message)
            return None
        data = self._dbOperate.getTagsByPostID(postID)  # data的格式: [tag_name, ...]
        # 这里转换成前端chip组件data参数需要的数据格式: [ { tag: tag_name }, ...]
        tempRes = []
        for tag in data:
            tempRes.append({'tag': tag})
        message['result'] = tempRes
        self.write(message)
