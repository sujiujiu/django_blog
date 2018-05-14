# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
import uuid
import hashers

class FrontUserModel(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4)
    telephone = models.CharField(max_length=11,unique=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20)
    _password = models.CharField(max_length=128)
    avatar = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __init__(self,*args,**kwargs):
        if 'password' in kwargs:
            hash_password = hashers.make_password(kwargs['password'])
            kwargs['password'] = hash_password
        super(FrontUserModel,self).__init__(*args,**kwargs)

    # property将方法变成一个属性，适用于没有参数的函数
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = self.set_password(raw_password)

    def check_password(self,raw_password):
        # raw_password是指密码的原始字符串
        return hashers.check_password(raw_password,self.password)

    def set_password(self,raw_password):
        if not raw_password:
            return None

        hash_password = hashers.make_password(raw_password)
        self._password = hash_password
        self.save(update_fields=['password'])


