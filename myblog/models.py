# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class ArticleModel(models.Model):
    # 如果一个field传了editable=False，那么调用diaogo的model_to_dict的时候会丢失这个字段
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4)
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    thumbnail = models.URLField(max_length=200)
    content = models.TextField()
    # auto_now_add只会在第一次存入当前时间，之后不会修改该值
    create_time = models.DateTimeField(auto_now_add=True,null=True)
    # auto_now每次修改都会更新当前时间
    update_time = models.DateTimeField(auto_now=True,null=True)
    read_count = models.IntegerField(default=0)
    is_removed = models.BooleanField(required=False)
    
    author = models.ForeignKey(User, null=False)
    # board = models.ForeignKey('BoardModel', null=True)
    category = models.ForeignKey('CategoryModel')
    top = models.ForeignKey('TopModel',null=True,on_delete=models.SET_NULL)
    tags = models.ManyToManyField('TagModel', blank=True)


# # 帖子相关模型
# class PostModel(models.Model):
#     uid = models.UUIDField(primary_key=True,default=uuid.uuid4)
#     title = models.CharField(max_length=100,null=False)
#     content = models.TextField(null=False)
#     create_time = models.DateTimeField(auto_now_add=True,null=True)
#     update_time = models.DateTimeField(auto_now=True,null=True)
#     read_count = models.IntegerField(default=0)
#     is_removed = models.BooleanField(default=False)
#     thumbnail = models.URLField(blank=True)

#     tags = models.ManyToManyField('TagModel', blank=True)
#     author = models.ForeignKey(User, null=True)
#     category = models.ForeignKey('CategoryModel')
#     board = models.ForeignKey('BoardModel')
#     highlight = models.ForeignKey('HighlightPostModel',null=True,on_delete=models.SET_NULL)


class TopModel(models.Model):
    # auto_now: save时就会更新
    # auto_now_add: 只有在第一次添加的时候才会修改这个字段
    create_time = models.DateTimeField(auto_now=True)

class CategoryModel(models.Model):
    name = models.CharField(max_length=20, unique=True)

class TagModel(models.Model):
    name = models.CharField(max_length=20, unique=True)

# 版块模型
class BoardModel(models.Model):
    name = models.CharField(max_length=20, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, null=True)


# 评论
class CommentModel(models.Model):
    content = models.TextField(null=False)
    create_time = models.DateTimeField(auto_now=True)
    is_removed = models.BooleanField(default=False)

    author = models.ForeignKey(User, null=True)
    post = models.ForeignKey('ArticleModel',null=False)
    comment = models.ForeignKey('CommentModel',null=True)


# 点赞
class ArticleStarModel(models.Model):
    create_time = models.DateTimeField(auto_now=True)
    post = models.ForeignKey('ArticleModel',null=False)
    author = models.ForeignKey(User, null=True)
