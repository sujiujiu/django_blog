# -*- coding: utf-8 -*-
# @Author: xiaotuo
# @Date:   2016-11-17 20:08:36
# @Last Modified by:   Administrator
# @Last Modified time: 2016-11-18 21:26:20
from __future__ import unicode_literals
import uuid
import hashlib
import configs

from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class FrontUserModel(models.Model):
	# 用户相关的表，不要使用自增长的id作为主键
	uid = models.UUIDField(primary_key=True,default=uuid.uuid4)
	email = models.EmailField(unique=True)
	username = models.CharField(max_length=20)
	_password = models.CharField(max_length=128)
	avatar = models.URLField(blank=True)
	is_active = models.BooleanField(default=True)
	date_joined = models.DateTimeField(auto_now_add=True)


	def __init__(self,*args,**kwargs):
		if 'password' in kwargs:
			kwargs['password'] = self.make_password(kwargs['password'])
		super(FrontUserModel,self).__init__(*args,**kwargs)

	@property
    def password(self):
        return self._password

    @password.setter
	def set_password(self,raw_password):
		if not raw_password:
			return None

		self._password = self.make_password(raw_password)
		self.save(update_fields=['password'])

	def make_password(raw_password, salt=None):
		if not salt:
			salt = configs.PASSWORD_SALT

		hash_password = hashlib.md5(salt+raw_password).hexdigest()
		return hash_password

	def set_check_password(raw_password, hash_password):
		# 首先需要对raw_password使用和创建用户时一样的加密算法来进行加密,
		# 而且使用的salt必须一样，
		# 然后再和数据库中的密码进行对比
		if not raw_password:
			return False

		tmp_password = self.make_password(raw_password)
		if tmp_password == hash_password:
			return True
		else:
			return False

	def check_password(self,raw_password):
		return self.set_check_password(raw_password,self.password)

	




