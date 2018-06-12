# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class ArticleModel(models.Model):
    # 如果一个field传了editable=False，那么调用diaogo的model_to_dict的时候会丢失这个字段
    article_id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    title = models.CharField(max_length=100)
    # desc = models.CharField(max_length=200)
    thumbnail = models.URLField(max_length=200)
    content = models.TextField()
    # auto_now_add只会在第一次存入当前时间，之后不会修改该值
    create_time = models.DateTimeField(auto_now_add=True,null=True)
    # auto_now每次修改都会更新当前时间
    update_time = models.DateTimeField(auto_now=True,null=True)
    read_count = models.IntegerField(default=0)
    is_removed = models.BooleanField(null=False,default=False)
    
    author = models.ForeignKey(User, null=False)
    # board = models.ForeignKey('BoardModel', null=True)
    category = models.ForeignKey('CategoryModel')
    # SET_NULL和CASCADE的区别在于，后者级联删除，而前者只是改为NULL
    # 设置ForeignKey 为 null; 这个只有设置了null 为 True的情况才能用
    top = models.ForeignKey('TopModel',null=True,on_delete=models.SET_NULL)
    tags = models.ManyToManyField('TagModel', blank=True)

    class Meta:
        ordering=['-create_time']


# 置顶
class TopModel(models.Model):
    # auto_now: save时就会更新
    # auto_now_add: 只有在第一次添加的时候才会修改这个字段
    create_time = models.DateTimeField(auto_now=True)

# 分类
class CategoryModel(models.Model):
    name = models.CharField(max_length=20, unique=True)

# 标签
class TagModel(models.Model):
    name = models.CharField(max_length=20, unique=True)


# 评论
class CommentModel(models.Model):
    content = models.TextField(null=False)
    create_time = models.DateTimeField(auto_now=True)
    is_removed = models.BooleanField(default=False)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey('ArticleModel', on_delete=models.CASCADE)
    reply_id = models.ForeignKey('CommentModel', related_name='reply', on_delete=models.CASCADE, null=True, blank=True)


# 点赞
class ArticleStarModel(models.Model):
    create_time = models.DateTimeField(auto_now=True)
    article = models.ForeignKey('ArticleModel')
    author = models.ForeignKey(User)
