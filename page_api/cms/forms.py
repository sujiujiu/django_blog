# -*- coding: utf-8 -*-
import json
from django import forms
from utils.captcha.mycaptcha import Captcha
from utils import myjson
from page_api.common.forms import BaseForm

class CMSLoginForm(forms.Form):
	username = forms.CharField(max_length=10, min_length=4)
	password = forms.CharField(max_length=20, min_length=6)
	captcha = forms.CharField(max_length=4,min_length=4)
	remember = forms.BooleanField(required=False) #用户有可能不需要记住我,那么这个参数有可能就没有

	def clean_captcha(self):
		captcha = self.cleaned_data.get('captcha',None)
		if not Captcha.check_captcha(captcha):
			raise forms.ValidationError(u'验证码错误!')
		return captcha

class UpdateProfileForm(BaseForm):
	avatar = forms.URLField(max_length=100,required=False)
	username = forms.CharField(max_length=10,min_length=4,required=False)


class UpdateEmailForm(BaseForm):
	email = forms.EmailField(required=True)


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

	
