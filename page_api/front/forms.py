# -*- coding: utf-8 -*-
from django import forms

class FrontLoginForm(forms.Form):
	username = forms.CharField(max_length=10, min_length=4)
	password = forms.CharField(max_length=20, min_length=6)
	remember = forms.BooleanField(required=False)
	captcha = forms.CharField(max_length=4,min_length=4)


class FrontRegistForm(forms.Form):
	'''注册的表单，手机号和手机验证码，都是数字，验证码6位的
	   max_length和min_length的值相同，等价于equal，即相等，意味着长度=这个值
	'''
	telephone = forms.IntegerField(max_length=11, min_length=11)
	password = forms.CharField(max_length=20, min_length=6)
	sms_captcha = forms.IntegerField(max_length=6, min_length=6)
