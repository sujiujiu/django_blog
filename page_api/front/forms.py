# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.core.validators import RegexValidator
from django.core.cache import cache

from page_api.common.forms import BaseForm
from utils.captcha.mycaptcha import Captcha

class CaptchaForm(forms.Form):
	captcha = forms.CharField(max_length=4,min_length=4)
	
	def clean_captcha(self):
		captcha = self.cleaned_data.get('captcha')
		if not Captcha.check_captcha(captcha):
			raise forms.ValidationError(u'验证码错误')

		return captcha

class FrontLoginForm(forms.Form):
	username = forms.CharField(max_length=10, min_length=4)
	password = forms.CharField(max_length=20, min_length=6)
	remember = forms.BooleanField(required=False)
	captcha = forms.CharField(max_length=4,min_length=4)


class FrontRegistForm(forms.Form):
	'''注册的表单，手机号和手机验证码，都是数字，验证码6位的
	   max_length和min_length的值相同，等价于equal，即相等，意味着长度=这个值
	'''
	telephone = forms.CharField(max_length=11,\
		validators=[RegexValidator("^1(3|4|5|7|8)\d{9}$","手机号码有误")])
	# password = forms.CharField(max_length=20, min_length=6)
	sms_captcha = forms.CharField(max_length=6)


class ForgetpwdForm(BaseForm,CaptchaForm):
	email = forms.EmailField()

class ResetEmailForm(BaseForm,CaptchaForm):
	email = forms.EmailField(required=True)
	captcha = forms.CharField(max_length=4,min_length=4,required=True)


class ResetpwdForm(BaseForm):
	oldpwd = forms.CharField(max_length=20, min_length=6)
	newpwd = forms.CharField(max_length=20, min_length=6)
	newpwd_repeat = forms.CharField(max_length=20,min_length=6)

	def clean(self):
		newpwd = self.cleaned_data.get('newpwd')
		newpwd_repeat = self.cleaned_data.get('newpwd_repeat')
		if newpwd != newpwd_repeat:
			raise forms.ValidationError(u'两个密码不一致')
		return self.cleaned_data


class AddCommentForm(BaseForm):
	content = forms.CharField(max_length=200)
	article_id = forms.CharField()


class ReplyCommentForm(BaseForm):
    article_id = forms.IntegerField(required=True)
    content = forms.CharField(max_length=200,min_length=1,required=True)
    comment_id = forms.IntegerField()


class AddArticleForm(BaseForm):
	title = forms.CharField(max_length=200)
	category = forms.IntegerField(required=True)
	# desc = forms.CharField(max_length=200,required=False)
	thumbnail = forms.URLField(max_length=100,required=False)
	content = forms.CharField()


class SettingsForm(BaseForm):
	avatar = forms.URLField(max_length=100,required=False)
	username = forms.CharField(max_length=20,min_length=4,required=False)
	realname = forms.CharField(max_length=10,min_length=2,required=False)
	qq = forms.CharField(max_length=20,min_length=5,required=False)
	signature = forms.CharField(max_length=30,min_length=1,required=False)
	gender = forms.IntegerField(required=False)


class ArticleStarForm(BaseForm):
	article_id = forms.UUIDField(error_messages={'required':u'必须输入文章id'})
	is_star = forms.BooleanField(required=True)

