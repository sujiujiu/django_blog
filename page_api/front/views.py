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
def front_reset_email(request):
    if request.method == 'GET':
        return render(request, 'front_reset_email.html')
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
            message = form.get_error()
            return myjson.json_params_error(message)

# 邮箱验证
def front_validate_email(request):
    pass

def front_profile(request):
    return render(request, 'front_profile.html')

def front_settings(request):
    if request.method == 'GET':
        return render(request, 'front_settings.html')
    else:
        pass


def front_reset_pwd(request):
    pass

def front_forget_pwd(request):
    pass

def front_qiniu_token(request):
    pass



# 文章相关操作

def front_article_list(request,page=1,sort=1,category_id=0):
    context = ArticleModelHelper.article_list(page, sort, category_id)
    return render(request, 'front_article_list.html',context)

def front_article_detail(request):
    pass

# 添加文章
def front_add_article(request):
    pass

# 编辑文章
def front_edit_article(request):
    pass

# 删除文章，和后端不同，前台只删除，但不真正删除
def front_remove_article(request):
    article_id = request.GET.get('article_id')
    article_model = ArticleModel.objects.filter(article_id=article_id)
    article_model.is_removed = True
    article_model.save()
    return redirect(reverse('article_list'))

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

def front_remove_comment(request):
    pass

def front_reply_comment(request):
    pass