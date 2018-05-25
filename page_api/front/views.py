# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import top

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
            email = form.cleaned_data.get('telephone')
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
    pass


# @front_login_required
def front_logout(request):
    logout(request)
    return redirect(reverse('front_index'))


# 修改邮箱
def front_reset_email(request):
    pass

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

# 短信验证码
def sms_captcha(request):
    telephone = request.GET.get('telephone')
    # 获取用户名，用于发送短信验证码显示用户名
    # username = flask.request.args.get('username')
    if not telephone:
        return myjson.json_params_error(message=u'必须指定手机号码！')
    if cache.get(telephone):
        return myjson.json_params_error(message=u'验证码已发送，请1分钟后重复发送！')
    # if not username:
    #     return myjson.json_params_error(message=u'必须输入用户名！')
    # 阿里大于APP_KEY及APP_SECRET
    app_key = settings.APP_KEY
    app_secret = settings.APP_SECRET
    req = top.setDefaultAppInfo(app_key, app_secret)
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.extend = ""
    req.sms_type = 'normal'
    # 签名名称
    req.sms_free_sign_name = settings.SIGN_NAME
    # 随即生成字符串
    captcha = Captcha.gene_text()
    # 设置短信的模板
    req.sms_param = "{code:%s}" % captcha
    # req.sms_param = "{username:%s,code:%s}" % (username, captcha)
    req.rec_num = telephone.decode('utf-8').encode('ascii')
    req.sms_template_code = settings.TEMPLATE_CODE
    try:
        resp = req.getResponse()
        cache.set(telephone, captcha, 120)
        return myjson.json_result()
    except Exception, e:
        print e
        return myjson.json_server_error()


# 文章相关操作

def front_article_list(request):
    pass

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