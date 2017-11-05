# coding: utf8
from models.tags import Model as tagModel
from models.posts import Model as postModel
from models.post_tags import Model as postTagsModel
from models import db


class Model(object):

    def __init__(self, dbSession):
        self._session = dbSession

    def getPostLists(self):
        raw = self._session.query(postModel.post_id, postModel.post_title, postModel.post_summary,
                                  postModel.post_is_draft).order_by(db.DESC(postModel.post_create_timestamp)).all()
        return raw

    def getPostInfoByID(self, postID):
        try:
            raw = self._session.query(postModel).filter(postModel.post_id==postID).one()
            tagList = self.getTagsByPostID(postID)
            return {
                'post': raw,
                'tags': tagList
            }
        except Exception, e:
            return False

    def updatePostInfo(self, postID, title, author, summary, content, isDraft, isHidden, tags):
        """更新文章信息"""
        info = self.getPostInfoByID(postID)
        if not info:
            return False

        postInfo = info['post']
        postInfo.post_title = title
        postInfo.post_summary = summary
        if postInfo.post_author != author:
            postInfo.post_author = author
        postInfo.post_content = content
        if isDraft and isDraft != '0':
            postInfo.post_is_draft = 1
        else:
            postInfo.post_is_draft = 0
        if isHidden and isHidden != '0':
            postInfo.post_is_hidden = 1
        else:
            postInfo.post_is_hidden = 0

        try:
            self._session.commit()
            return True
        except Exception, e:
            self._session.rollback()
            return False

    def addPostByDict(self, info):
        """添加文章"""
        # 调整数据格式
        if info['post_is_draft'] and info['post_is_draft'] != '0':
            info['post_is_draft'] = 1
        else:
            info['post_is_draft'] = 0
        if info['post_is_hidden'] and info['post_is_hidden'] != '0':
            info['post_is_hidden'] = 1
        else:
            info['post_is_hidden'] = 0
        # 把文章标签写入tbl_tags表中
        tagIDsList = self.addTagByList(info.pop('tag_name'))

        # 文章内容写入tbl_posts表中
        postRecord = postModel(**info)
        try:
            self._session.add(postRecord)
            self._session.commit()
        except Exception, e:
            self._session.rollback()
            return False

        # 在tbl_post_tags表中添加文章与标签的关联
        for tagID in tagIDsList:
            record = postTagsModel(tbl_posts_post_id=postRecord.post_id, tbl_tags_tag_id=tagID)
            try:
                self._session.add(record)
            except Exception, e:
                continue
        self._session.commit()
        return True

    def deletePostByID(self, postID):
        """根据文章ID删除文章"""
        postInfo = self.getPostInfoByID(postID)
        if not postInfo:
            return False

        try:
            self._session.delete(postInfo)
            self._session.commit()
            return True
        except Exception, e:
            self._session.rollback()
            return False

    def addTagByList(self, tagsList):
        """根据输入的标签列表循环添加标签到标签表中"""
        result = []
        for tag in tagsList:
            record = tagModel(tag_name=tag)
            try:
                self._session.add(record)
                self._session.flush()
                result.append(record.tag_id)
            except Exception, e:
                continue
        self._session.commit()
        return result

    def getTagsByPostID(self, postID):
        result = []
        raw = self._session.query(tagModel).join(postTagsModel, tagModel.tag_id==postTagsModel.tbl_tags_tag_id).\
            filter(postTagsModel.tbl_posts_post_id == postID).all()
        for tag in raw:
            result.append(tag.tag_name)
        return result

    def getAllTags(self):
        raw = self._session.query(tagModel).all()
        return raw
