# -*- coding: utf-8 -*-
import top

from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from django.core.cache import cache
from django.conf import settings
from django.views.decorators.http import require_http_methods

from frontauth.decorators import front_login_required

from utils.captcha.mycaptcha import Captcha
from utils import myjson
import qiniu

from PIL import Image
try:
	from cStringIO import StringIO
except ImportError:
	from io import BytesIO as StringIO

# 图形验证码
def graph_captcha(request):
	text,image = Captcha.gene_code()
	out = StringIO() 
	# 将StringIO的指针指向开始的位置
    out.seek(0)
    # 指定响应的类型
    response = HttpResponse(content_type='image/png')
    # 把图片流给读出来
    response.write(out.read())
    return response


# 短信验证码
def sms_captcha(request):
    telephone = request.GET.get('telephone')
    # 获取用户名，用于发送短信验证码显示用户名
    if not telephone:
        return myjson.json_params_error(message=u'必须指定手机号码！')
    if cache.get(telephone):
        return myjson.json_params_error(message=u'验证码已发送，请1分钟后重复发送！')
    # if not username:
    #     return myjson.json_params_error(message=u'必须输入用户名！')
    # 阿里大于APP_KEY及APP_SECRET
    app_key = settings.APP_KEY
    app_secret = settings.APP_SECRET
    request = top.setDefaultAppInfo(app_key, app_secret)
    request = toprequest.api.AlibabaAliqinFcSmsNumSendRequest()
    request.extend = ""
    request.sms_type = 'normal'
    # 签名名称
    request.sms_free_sign_name = settings.SIGN_NAME
    # 随即生成字符串
    captcha = Captcha.gene_text()
    # 设置短信的模板
    request.sms_param = "{code:%s}" % captcha
    # request.sms_param = "{username:%s,code:%s}" % (username, captcha)
    request.rec_num = telephone.decode('utf-8').encode('ascii')
    request.sms_template_code = settings.TEMPLATE_CODE
    try:
        resp = request.getResponse()
        cache.set(telephone, captcha, 120)
        return myjson.json_result()
    except Exception, e:
        print e
        return myjson.json_server_error()


@front_login_required
@require_http_methods(['GET'])
def qiniu_token(request):
    # 授权
    q = qiniu.Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
    # 选择七牛的云空间
    bucket_name = 'myblog-article'
    # 生成token
    token = q.upload_token(bucket_name)
    return myjson.json_result({'uptoken': token})