# -*- coding: utf-8 -*-
import json
from django import forms
from utils.captcha.mycaptcha import Captcha
from utils import myjson
from page_api.common.forms import BaseForm


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

	def clean(self):
		password = self.cleaned_data.get('password')
		password_repeat = self.cleaned_data.get('password_repeat')
		if password != password_repeat:
			raise forms.ValidationError(u'两个密码不一致')
		return self.cleaned_data


class AddCategoryForm(BaseForm):
	categoryname = forms.CharField(max_length=20)

class AddTagForm(BaseForm):
	tagname = forms.CharField(max_length=20)

class AddArticleForm(BaseForm):
	title = forms.CharField(max_length=200)
	category = forms.IntegerField(required=True)
	desc = forms.CharField(max_length=200,required=False)
	thumbnail = forms.URLField(max_length=100,required=False)
	content_html = forms.CharField()

class UpdateArticleForm(AddArticleForm):
	uid = forms.UUIDField()


class DeleteArticleForm(BaseForm):
	uid = forms.UUIDField(error_messages={'required':u'文章id不能少'})

class TopArticleForm(DeleteArticleForm):
	pass

class CategoryForm(BaseForm):
	category_id = forms.IntegerField()

class EditCategoryForm(CategoryForm):
	name = forms.CharField()

	
