# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CmsUserModel(models.Model):
	avatar = models.URLField(max_length=100,blank=True)
	# django中的User模型必须和CmsUser中一对一的对应
	user = models.OneToOneField(User)