# -*- coding: utf-8 -*-
import json
from django import forms
from utils.captcha.mycaptcha import Captcha
from utils import myjson
from page_api.common.forms import BaseForm
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class CMSLoginForm(BaseForm):
	username = forms.CharField(max_length=10, min_length=4)
	password = forms.CharField(max_length=20, min_length=6)
	captcha = forms.CharField(max_length=4,min_length=4)
	remember = forms.BooleanField(required=False)

	def clean_captcha(self):
		captcha = self.cleaned_data.get('captcha',None)
		if not Captcha.check_captcha(captcha):
			raise forms.ValidationError(u'验证码错误!')
		return captcha

class SettingsForm(BaseForm):
	avatar = forms.URLField(max_length=100,required=False)
	username = forms.CharField(max_length=10,min_length=4,required=False)


class ResetEmailForm(BaseForm):
	email = forms.EmailField(required=True)

class ResetpwdForm(BaseForm):
	oldpwd = forms.CharField(max_length=20, min_length=6)
	newpwd = forms.CharField(max_length=20, min_length=6)
	newpwd_repeat = forms.CharField(max_length=20,min_length=6)

	def __init__(self, user, *args, **kwargs):
	# def __init__(self, username, *args, **kwargs):
		# self.username = username
		self.user = user
		super(ResetpwdForm, self).__init__(*args, **kwargs)

	def clean(self):
		newpwd = self.cleaned_data.get('newpwd')
		newpwd_repeat = self.cleaned_data.get('newpwd_repeat')
		if newpwd != newpwd_repeat:
			raise forms.ValidationError(u'两个密码不一致')
		return self.cleaned_data

    def save_password(self):
		oldpwd = self.cleaned_data.get('oldpwd')
		newpwd = self.cleaned_data.get('newpwd')
		is_vaild = self.user.check_password(oldpwd)
		if vaild:
			self.user.set_password(newpwd)
			self.user.save()
		else:
            raise forms.ValidationError("密码错误")
         return valid

	def cleaned_password(self):
		oldpwd = self.cleaned_data.get('oldpwd')
		newpwd = self.cleaned_data.get('newpwd')
		user = authenticate(username=self.username,password=oldpwd)
		if user:
			is_vaild = user.check_password(oldpwd)
			if is_vaild:
				user.set_password(newpwd)
				user.save()
			else:
				raise forms.ValidationError(u'密码错误')
		else:
			user = user.create(username=username,password=newpwd)
		return user


class TagForm(BaseForm):
	tag_id = forms.IntegerField()

class AddTagForm(BaseForm):
	tag_name = forms.CharField(max_length=20)

class AddArticleForm(BaseForm):
	title = forms.CharField(max_length=200)
	category = forms.IntegerField(required=True)
	# desc = forms.CharField(max_length=200,required=False)
	thumbnail = forms.URLField(max_length=100,required=False)
	content = forms.CharField()

class EditArticleForm(AddArticleForm):
	article_id = forms.UUIDField()

class DeleteArticleForm(BaseForm):
	article_id = forms.UUIDField(error_messages={'required':u'必须输入文章id'})


class TopArticleForm(DeleteArticleForm):
	pass

class CategoryForm(BaseForm):
	category_id = forms.IntegerField()

class AddCategoryForm(BaseForm):
	categoryname = forms.CharField(max_length=20)

class EditCategoryForm(CategoryForm):
	name = forms.CharField()

	
class DeleteCommentForm(BaseForm):
	comment_id = forms.UUIDField()