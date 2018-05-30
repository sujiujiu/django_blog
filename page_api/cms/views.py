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
from django.forms.models import model_to_dict
from django.db.models import Count

from forms import CMSLoginForm,SettingsForm,ResetEmailForm,ResetpwdForm,\
				AddCategoryForm,AddTagForm,AddArticleForm,UpdateArticleForm,\
				DeleteArticleForm,TopArticleForm,CategoryForm,EditCategoryForm

from myblog.models import ArticleModel,CategoryModel,TagModel,TopModel,\
				CommentModel,ArticleStarModel,BoardModel
from cmsauth.models import CmsUserModel
from common.basemodels import ArticleModelHelper

from utils.myemail import send_email
from utils import myjson
import qiniu
import qiniu.config


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
		# 如果邮箱在数据库存在，则无需修改
		# 否则才允许修改新密码
		form = ResetEmailForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email', None)
			if email:
				if request.email == email:
					return myjson.json_params_error(u'新邮箱与老邮箱一致，无需修改！')
				else:
					if send_mail(receivers=email):
						return myjson.json_result(u'该邮箱已经发送验证码了！')
				    else:
				        return myjson.json_server_error()
	        else:
	        	message = form.get_error()
	            return myjson.json_params_error(message)
		else:
			return render(request,'cms_reset_email.html',{'error':form.errors})

# 邮箱验证
@login_required
def cms_validate_email(request, email):
	# cache的保存期设置为2分钟，如果还能获取，则说明验证码已发送
	# 否则链接失效
	if cache.get(email):
		user = request.user
		user.email = email
		user.save(update_fields=['email'])
		return myjson.json_result(u'该邮箱验证成功！')
	else:
		return myjson.json_params_error(u'链接已失效！')

# 修改密码
@login_required
def cms_reset_pwd(request):
	if request.method == 'GET':
		return render(request, 'cms_reset_pwd.html')
	else:
		username = request.user
		## 使用cleaned_password方法
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
			# user = User.objects.all().first()
			user = request.user
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
			return myjson.json_params_error(message)


@login_required
@require_http_methods(['GET'])
def cms_qiniu_token(request):
	# 授权
    q = qiniu.Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
    # 选择七牛的云空间
    bucket_name = 'myblog-article'
    # 生成token
    token = q.upload_token(bucket_name)
    return myjson.json_result({'uptoken': token})


### 文章管理


## 文章操作

# 文章列表
@login_required
def cms_article_list(request,page=1,sort=1,category_id=0):
	context = ArticleModelHelper.article_list(page, sort, category_id)
	return render(request, 'cms_article_list.html',context)

# 添加文章
@login_required
def cms_add_article(request):
	# 1.请求页面时，我们需要获取所有的标签和分类
	# 2.提交修改后的页面时，检查分类和标签在数据库中是否存在，
	# 如果不存在则新建，否则存入
	# 3.文章与标签是多对多关系，与其他内容不一起存
	# 4.文章与分类不是是多对多关系
	if request.method == 'GET':
		tags = TagModel.objects.all()
		categorys = CategoryModel.objects.all()
		context = {
			'tags':tags,
			'categorys':categorys
		}
		return render(request, 'cms_add_article.html', context)
	else:
		form = AddArticleForm(request.POST)
		if form.is_valid():
			user = request.user
			tag_ids = request.POST.getlist('tags[]')

			title = form.cleaned_data.get('title')
			thumbnail = form.cleaned_data.get('thumbnail')
			content = form.cleaned_data.get('content')
			category_id = form.cleaned_data.get('category')

			category = CategoryModel.objects.filter(pk=category_id).first()

			article_model = ArticleModel(
				username=user,
				title=title,
				thumbnail=thumbnail,
				content=content,
				category=category
				)
			article_model.save()
			# 文章与标签的多对多的保存
			# 如果选择了标签，则将选择的标签以此存入，否则不用存
			if tag_ids:
				for tag_id in tag_ids:
					tag_model = TagModel.objects.filter(pk=tag_id).first()
					if tag_model:
						article_model.tags.add(tag_model)
			return myjson.json_result()
		else:
			message = form.errors
			return myjson.json_params_error(message)

			
# 编辑文章
@login_required
def cms_edit_article(request, article_id):
	'''
	   它的逻辑和add_article相似，但作者不会变，只需获取文章的id
	   我们会用到一篇已存在的article里的的所有数据，包括tags
	   但文章里的tags会通过article.tags多对多的方式获取，而不再从tagmodel获取
	   因为可能会修改tags，我们仍需要传入所有的tags
	   因此我们需要将tags添加到article里，而为了方便使用，也为了添加tags
	   我们会使用到model_to_dict这个函数，将数据库里的数据提取出来并转化成dict类型
	'''
	if request.method == 'GET':
		article_model = ArticleModel.objects.filter(pk=article_id).first()
		article_dict = model_to_dict(article_model)
		tag_model = article_model.tags.all()
		article_dict['tags'] = [tag_model.id for tags in tag_model]
		context = {
			'categorys': CategoryModel.objects.all(),
			'tags': TagModel.objects.all(),
			'article': article_dict
		}
		return render(request, 'cms_add_article.html', context)
	else:
		form = EditArticleForm(request.POST)
		if form.is_valid():
			tag_ids = request.POST.getlist('tags[]')

			article_id = form.cleaned_data.get('article_id')
			title = form.cleaned_data.get('title')
			thumbnail = form.cleaned_data.get('thumbnail')
			content = form.cleaned_data.get('content')
			category_id = form.cleaned_data.get('category')

			article_model = ArticleModel.objects.filter(pk=article_id).first()
			category = CategoryModel.objects.filter(pk=category_id).first()

			# 修改和创建的方式不一样
			if article_model:
				article_model.title = title
				article_model.thumbnail = thumbnail
				article_model.content = content
				article_model.category = category
				article_model.save()

			# 文章与标签的多对多的保存
			# 如果选择了标签，则将选择的标签以此存入，否则不用存
			if tag_ids:
				for tag_id in tag_ids:
					tag_model = TagModel.objects.filter(pk=tag_id).first()
					if tag_model:
						article_model.tags.add(tag_model)
			return myjson.json_result()
		else:
			message = form.errors
			return myjson.json_params_error(message)


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
@login_required
def cms_top_article(request):
	'''
		1. 不管数据库中该文章是否已经置顶，都保存，这样可以更改文章修改时间
		2. 如果没有置顶则置顶，有则直接保存
		3. 修改TopModel，之后也要更改ArticleModel，只需要更改top字段
	'''
	form = TopArticleForm(request.POST)
	if form.is_valid():
		article_id = form.cleaned_data.get('article_id')
		article_model = ArticleModel.objects.filter(pk=article_id).first()
		if article_model:
			top_model = article_model.top
			if not top_model:
				top_model = TopModel()
			top_model.save()

			article_model.top = top_model
			article_model.save(update_fields=['top'])
			return myjson.json_result()
		else:
			return myjson.json_params_error(u'文章不存在！')
	else:
		message = form.errors
		return myjson.json_params_error(message)


## 评论管理
@login_required
def cms_comment_list(request, page=1):
	context = ArticleModelHelper.common_page(page=page, model_name=CommentModel,key_name='comments')
	return render(request, 'cms_comment_list.html',context)

@login_required
@require_http_methods(['POST'])
def cms_remove_comment(request):
	comment_id = request.POST.get('comment_id',1)
    if not comment_id:
        return myjson.json_params_error()
    comment_model = CommentModel.objects.filter(comment_id).first()
    if comment_model:
    	comment_model.is_removed = True
    	comment_model.save()
    return myjson.json_result()



## tag标签管理

# 标签管理列表
@login_required
def cms_tag_list(request):
	tags = TagModel.objects.all()
	return render(request, 'cms_tag_list.html', {'tags':tags})

# 增加标签
@login_required
@require_http_methods(['POST'])
def cms_add_tag(request):
	'''如果tag已经存在，则不允许在添加，否则添加
	'''
	form = AddTagForm(request.POST)
	if form.is_valid():
		tag_name = form.cleaned_data.get('tag_name')
		tag_model = TagModel.objects.filter(name=tag_name).first()
		if tag_model:
			return myjson.json_params_error(u'该标签已存在，请重新设置！')
		else:
			tagModel = TagModel(name=tag_name)
			tagModel.save()
			return myjson.json_result()
	else:
		message = form.errors
		return myjson.json_params_error(message)


# 移除标签
@login_required
@require_http_methods(['POST'])
def cms_remove_tag(request):
	'''
	1.如果该标签不存在不能移除，
	2.如果标签下有文章则不允许移除，
	因此我们要获取该标签下的所有文章，如果文章数小于0则不允许删除
	'''
	form = TagForm(request.POST)
	if form.is_valid():
		tag_id = form.cleaned_data.get('tag_id')
		tag_model = TagModel.objects.filter(pk=tag_id).first()
		if tag_model:
			article_count = tag_model.articlemodel_set.all().count()
			if article_count > 0:
				return myjson.json_params_error(message=u'该标签下还有文章,不能删除!')
			else:
				tag_model.delete()
				return myjson.json_result()
		else:
			return myjson.json_params_error(message=u'该标签不存在！')
	else:
		message = form.errors
		return myjson.json_params_error(message)
	

## 分类操作

# 分类管理列表
@login_required
def cms_category_list(request):
	categorys = CategoryModel.objects.all()
	return render(request, 'cms_category_list.html', {'categorys':categorys})

# 增加分类
@login_required
@require_http_methods(['POST'])
def cms_add_category(request):
	'''如果tag已经存在，则不允许在添加，否则添加
	'''
	form = AddCategoryForm(request.POST)
	if form.is_valid():
		category_name = form.cleaned_data.get('category_name')
		category_model = CategoryModel.objects.filter(name=category_name).first()
		if category_model:
			return myjson.json_params_error(u'该分类已存在，请重新设置！')
		else:
			categoryModel = categoryModel(name=category_name)
			categoryModel.save()
			return myjson.json_result()
	else:
		message = form.errors
		return myjson.json_params_error(message)

# 编辑分类
@login_required
@require_http_methods(['POST'])
def cms_edit_category(request):
	form = EditCategoryForm(request.POST)
	if form.is_valid():
		category_id = form.cleaned_data.get('category_id')
		category_name = form.cleaned_data.get('category_name')
		category_model = CategoryModel.objects.filter(pk=category_id).first()
		if category_model:
			category_model.name = name
			category_model.save(update_fields=['name'])
			return myjson.json_result()
		else:
			return myjson.json_params_error(message=u'该分类不存在')
	else:
		message = form.errors
		return myjson.json_params_error(message)

# 移除分类
@login_required
def cms_remove_category(request):
	'''
	1.如果该分类不存在不能移除，
	2.如果分类下有文章则不允许移除，
	因此我们要获取该分类下的所有文章，如果文章数小于0则不允许删除
	'''
	form = CategoryForm(request.POST)
	if form.is_valid():
		category_id = form.cleaned_data.get('category_id')
		category_model = CategoryModel.objects.filter(pk=category_id).first()
		if category_model:
			article_count = category_model.articlemodel_set.all().count()
			if article_count > 0:
				return myjson.json_params_error(message=u'该分类下还有文章,不能删除!')
			else:
				category_model.delete()
				return myjson.json_result()
		else:
			return myjson.json_params_error(message=u'该分类不存在！')
	else:
		message = form.errors
		return myjson.json_params_error(message)