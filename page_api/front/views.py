# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import top

import settings
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.core.cache import cache

from frontauth import configs
from frontauth.decorators import front_login_required
from forms import FrontLoginForm,FrontRegistForm,ForgetpwdForm,ResetpwdForm,CommentForm
from models import FrontUserModel
from utils import myjson



def front_index(request):
	return render(request, 'cms_index.html')

def front_login(request):
	if request.method == 'GET':
		return render(request,'front_signin.html')
	else:
		form = FrontLoginForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('telephone')
			password = form.cleaned_data.get('password')
			remember = form.cleaned_data.get('remember')

			user = FrontUserModel.objects.filter(email=email).first()
			if user and user.check_password(password):
				request.session[configs.LOGINED_KEY] = str(user.uid)
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


@front_login_required
def front_logout(request):
	try:
		del request.session[configs.LOGINED_KEY]
	except KeyError:
		pass


# 短信验证码
@bp.route('/sms_captcha/')
def sms_captcha():
    telephone = request.GET.get('telephone')
    # 获取用户名，用于发送短信验证码显示用户名
    # username = flask.request.args.get('username')
    if not telephone:
        return myjson.json_params_error(message=u'必须指定手机号码！')
    if xtcache.get(telephone):
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