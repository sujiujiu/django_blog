# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.core.cache import cache
from django.core import mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.forms import model_to_dict
from django.db.models import Count

from qiniu import Auth,put_file
import qiniu.config

from forms import CMSLoginForm,SettingsForm,ResetEmailForm,ResetpwdForm,\
				AddCategoryForm,AddTagForm,AddArticleForm,UpdateArticleForm,\
				DeleteArticleForm,TopArticleForm,CategoryForm,EditCategoryForm

from myblog.models import ArticleModel,CategoryModel,TagModel,TopModel,\
				CommentModel,ArticleStarModel,BoardModel
from cmsauth.models import CmsUserModel
from utils.myemail import send_email
from utils import myjson


# CMS用户管理

@login_required
def cms_index(request):
	return render(request, 'cms_index.html')

# 如果使用的是类定义的view，不能使用@login_required
def cms_login(request):
	if request.method == 'GET':
		return render(request, 'cms_login.html')
	else:
		# 1.获取表单
		# 2.验证表单
		# 3.如果表单存在则获取输入框中的账号密码
		# 4.验证与本地账号密码是否相等，如相等跳转到主页，否则报错
		form = CMSLoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username',None)
			password = form.cleaned_data.get('password',None)
			remember = form.cleaned_data.get('remember',None)
			user = authenticate(username=username,password=password)
			if user:
				login(request, user)
				if remember:
					# 设置None，默认时间是14天
					request.session.set_expiry(None)
				else:
					# 设置为0，意思是浏览器一旦关闭,session就会过期
					request.session.set_expiry(0)
				# 用于退出后重定向
				nexturl = request.GET.get('next',None)
				if nexturl:
					return redirect(nexturl)
				else:
					return redirect(reverse('cms_index'))
			else:
				return render(request, 'cms_login.html', {'error':u'用户名或密码错误!'})
				# return render(request,'cms_login.html',{'msg':u'用户名或密码错误!'})
		else:
			return render(request, 'cms_login.html', {'error':form.get_error()})
			
# 注销
@login_required
def cms_logout(request):
	logout(request)
	return redirect(reverse('cms_login'))

# 修改邮箱
@login_required
def cms_reset_email(request):
	if request.method == 'GET':
		return render(request, 'cms_reset_email.html')
	else:
		# 如果旧密码在数据库存在，则允许修改新密码
		form = ResetEmailForm(request.POST)
		if form.is_valid():
			pass
		else:
			return render(request,'cms_reset_email.html',{'error':form.errors})

# 邮箱验证
def cms_validate_email(request):
	pass

# 修改密码
@login_required
def cms_reset_pwd(request):
	if request.method == 'GET':
		return render(request, 'cms_reset_pwd.html')
	else:
		username = request.user
		# 使用cleaned_password方法
		# form = ResetpwdForm(request.POST,username=username)
		# return render(request,'cms_reset_pwd.html',{'error':form.errors})
		# 使用save_password方法
		form = ResetpwdForm(request.POST,user=username)
		if form.is_vaild():
			oldpwd = form.cleaned_data.get('oldpwd')
			user = authenticate(username=username,password=oldpwd)
			if user:
				is_vaild = form.save_password()
				if is_vaild:
					return myjson.json_result()
				else:
					return myjson.json_params_error(message=u'密码验证错误！')
			else:
				user = user.create(username=username,password=newpwd)
				return myjson.json_result()
		else:
			message = form.errors
			return xtjson.json_params_error(message)

@login_required
def cms_profile(request):
	return render(request, 'cms_profile.html')

@login_required
def cms_settings(request):
	# 1.默认User表里是没有avatar，所以用到了CMSUser表
	# 2.CMSUser表和User表建立了一对一
	# 3.我们先查找CMSUser里的用户id
	# 4.如果用户存在则存储avatar，否则新建该用户并储存
	if request.method == 'GET':
		return render(request, 'cms_settings.html')
	else:
		form = SettingsForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username',None)
			avatar = form.cleaned_data.get('avatar',None)
			# 存储username
			user = User.objects.all().first()
			user.username = username
			user.save()
			# 存储avatar
			cms_user = CmsUserModel.objects.filter(user__pk=user.pk)
			if cms_user:
				cms_user.avatar = avatar
			else:
				CmsUserModel(user=user,avatar=avatar)
			cms_user.save()
			return myjson.json_result()
		else:
			message = form.errors
			return xtjson.json_params_error(message)


def cms_qiniu_token(request):
	pass


### 文章管理


## 文章操作

# 文章列表
@login_required
def cms_article_list(request):
	pass

# 添加文章
@login_required
def cms_add_article(request):
	pass

# 编辑文章
@login_required
def cms_edit_article(request):
	if request.method == 'GET':
		return render(request, 'cms_add_article.html')
	else:
		form = AddArticleForm(request.POST)
		if form.is_valid():
			pass
		else:
			return render(request, 'cms_add_article.html',{'error':form.errors})


# 删除文章，后台删除即真正从数据库中删除
@login_required
@require_http_methods(['POST'])
def cms_delete_article(request):
	form = DeleteArticleForm(request.POST)
	if form.is_valid():
		article_id = form.cleaned_data.get('article_id')
		article_model = ArticleModel.objects.filter(pk=article_id).first()
		if article_model:
			article_model.delete()
			return myjson.json_result()
		else:
			return myjson.json_params_error(message=u'该文章不存在或已被删除')
	else:
		# return myjson.json_params_error(message=form.errors)
		return redirect(reverse('article_list'))



# 文章置顶
def cms_top_article(request):
	pass



## 评论管理

def cms_comment_list(request):
	pass

@login_required
def cms_remove_comment(request):
	pass



## 板块管理

def cms_board_list(request):
	pass

@login_required
def cms_add_board(request):
	pass

@login_required
def cms_edit_board(request):
	pass

@login_required
def cms_remove_board(request):
	pass



## tag标签管理

@login_required
def cms_add_tag(request):
	pass

@login_required
def cms_remove_tag(request):
	pass



## 分类操作

def cms_category_list(request):
	pass

@login_required
def cms_add_category(request):
	pass

@login_required
def cms_edit_category(request):
	pass

@login_required
def cms_remove_category(request):
	pass