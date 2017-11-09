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

        # 同步更新文章关联的标签
        if tags:
            self.setPostTagsByPostID(postID, tags)

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
            self._session.delete(postInfo['post'])
            self._session.commit()
            return True
        except Exception, e:
            self._session.rollback()
            return False

    def addTagByList(self, tagsList):
        """根据输入的标签列表循环添加标签到标签表中"""
        result = []
        for tag in tagsList:
            tag = tag.strip()
            if not tag:
                continue
            record = tagModel(tag_name=tag)
            try:
                self._session.add(record)
                self._session.flush()
                result.append(record.tag_id)
            except Exception, e:
                continue
        self._session.commit()
        return result

    def setPostTagsByPostID(self, postID, newTags):
        """编辑文章时更新文章标签"""
        allTags = self.getAllTags()
        allTagsList = {}
        for tagModel in allTags:
            allTagsList[tagModel.tag_name] = tagModel.tag_id
        # 将新的标签集与所有标签集做差集，得出需要插入到tbl_tags表的标签
        insertTagsList = list(set(newTags).difference(set(allTagsList.keys())))
        if insertTagsList:
            insertedTagsResult = self.addTagByList(insertTagsList)  # 已新增标签的标签ID列表
        else:
            insertedTagsResult = []
        # 删除该文章的所有标签关联记录
        self._session.query(postTagsModel).filter(postTagsModel.tbl_posts_post_id==postID).delete()
        # 将newTags中的已存在标签与allTagsList做交集，得出已存在标签的tag_id
        mixedNameList = list(set(newTags).intersection(set(allTagsList.keys())))
        mixedIDlist = [allTagsList.pop(mixedName) for mixedName in mixedNameList]
        # 与已新增标签的标签ID列表做合并操作
        mixedIDlist.extend(insertedTagsResult)
        # 遍历 mixedIDlist添加文章与标签关联关系
        for tagID in mixedIDlist:
            tempModel = postTagsModel(tbl_posts_post_id=postID, tbl_tags_tag_id=tagID)
            self._session.add(tempModel)
        try:
            self._session.commit()
            return True
        except Exception, e:
            self._session.rollback()
            return False

    def getTagsByPostID(self, postID):
        """根据文章ID获取该文章关联的所有标签"""
        result = []
        raw = self._session.query(tagModel.tag_name).join(postTagsModel, tagModel.tag_id==postTagsModel.tbl_tags_tag_id).\
            filter(postTagsModel.tbl_posts_post_id == postID).all()
        for tag in raw:
            result.append(tag.tag_name)
        return result

    def getAllTags(self):
        result = []
        for tag in self._session.query(tagModel).all():
            result.append(tag)
        return result
