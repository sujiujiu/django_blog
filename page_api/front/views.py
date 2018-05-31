# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.core.cache import cache
from django.views.decorators.http import require_http_methods

from frontauth import configs
from frontauth.decorators import front_login_required
from frontauth.utils import login,logout
from forms import FrontLoginForm,FrontRegistForm,ForgetpwdForm,ResetpwdForm,CommentForm
from frontauth.models import FrontUserModel
from common.basemodels import ArticleModelHelper

from utils import myjson, myemail
from utils.myemail import send_email

# 个人设置

def front_index(request):
    return render(request, 'front_index.html')

def front_login(request):
    if request.method == 'GET':
        return render(request,'front_login.html')
    else:
        form = FrontLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')

            user = login(request,email,password)
            if user and user.check_password(password):
                # request.session[configs.LOGINED_KEY] = str(user.uid)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                # 跳转到
                nexturl = request.GET.get('next')
                if nexturl:
                    return redirect(nexturl)
                else:
                    return redirect(reverse('front_index'))
            else:
                return render(request,'front_login.html',{"error":u'用户名和密码错误'})
        else:
            return render(request,'front_login.html',{'error':form.get_error()})


def front_regist(request):
    if request.method == 'GET':
        return render(request,'front_regist.html')
    else:
        form = FrontLoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            user = FrontRegistForm(telephone=telephone)
            user.save()
            return redirect(reverse('front_index')) 
        else:
            message = form.get_error()
            return myjson.json_params_error(message)


@front_login_required
def front_logout(request):
    logout(request)
    return redirect(reverse('front_index'))


# 修改邮箱
@front_login_required
def front_reset_email(request):
    if request.method == 'GET':
        return render(request, 'front_reset_email.html')
    else:
        # 如果邮箱在数据库存在，则无需修改
        # 否则才允许修改新密码
        form = ResetEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email', None)
            user = request.user
            if email:
                if request.email == email:
                    return myjson.json_params_error(u'新邮箱与老邮箱一致，无需修改！')
                else:
                    if send_mail(receivers=email):
                        user.email = email
                        user.save(update_fields=['email'])
                        return myjson.json_result(u'该邮箱验证成功！')
                    else:
                        return myjson.json_server_error()
            else:
                return myjson.json_params_error(message=u'必须输入邮箱！')
        else:
            message = form.get_error()
            return myjson.json_params_error(message)


def front_profile(request):
    return render(request, 'front_profile.html')

@front_login_required
def front_settings(request):
    if request.method == 'GET':
        return render(request, 'front_settings.html')
    else:
        pass


@front_login_required
def front_reset_pwd(request):
    pass



@front_login_required
def front_forget_pwd(request):
    pass


@front_login_required
def front_qiniu_token(request):
    pass



'''## 文章相关操作
1.前端和后台不一样，前端可以通过获取url的方式获取id，
但后端不允许，没有类似flask.request.form.get的方法，
因此后台通过Form的方式，前台通过urls.py修改url路由。

2.前台的删除方式和后台有别：
    2.1 后台删除是真正的从数据库删除
    2.2 前端删除只是在数据库给一个is_removed的字段，
        如果为True则说明被移除，False说明未删除，
        通过查询的时候过滤获取所有未删除的文章/评论等
'''

# 文章列表
def front_article_list(request,page=1,sort=1,category_id=0):
    context = ArticleModelHelper.article_list(page, sort, category_id)
    return render(request, 'front_article_list.html',context)

# 文章详情页
def front_article_detail(request, article_id):
    '''我们需要获取的有：
       1. 文章(ArticleModel)
       2. 标签(TagModel)
       3. 分类(CategoryModel)
       4. 评论(CommentModel)
       5. 点赞(ArticleStarModel)
       另外，阅读量访问一次+1，还需获取当前的分类
    '''
    article_model = ArticleModel.objects.filter(pk=article_id,is_removed=False)
    if article_model:
        # 每次访问阅读量都+1
        article_model.read_count += 1
        article_model.save()
        # 获取所有给这篇文章点赞的作者
        star_author_ids = [star_model.author.id for star_model in article_model.stars]
        context = {
            'articles':article_model,
            'comments': article_model.commentmodel_set.all(),
            'tags': TagModel.objects.all(),
            'categorys': CategoryModel.objects.all(),
            # 当前文章分类
            'c_category': article_model.category,
            # 当前文章分类
            'c_tag': article_model.tags,
        }
    else:
        return myjson.json_params_error(u'该文章不存在！')

# 添加文章
@front_login_required
def front_add_article(request):
    pass

# 编辑文章
@front_login_required
def front_edit_article(request):
    pass

# 删除文章，和后端不同，前台只删除，但不真正删除
@front_login_required
def front_delete_article(request, article_id):
    article_model = ArticleModel.objects.filter(article_id=article_id).first()
    if article_model:
        article_model.is_removed = True
        article_model.save()
        return redirect(reverse('article_list'))
    else:
        return myjson.json_params_error(u'该文章不存在！')

# 文章置顶
def front_top_article(request):
    pass

# 文章点赞
def front_article_star(request):
    pass

def front_comment_list(request):
    pass

def front_add_comment(request):
    pass

def front_delete_comment(request):
    pass

def front_reply_comment(request):
    pass

def front_search(request):
    pass