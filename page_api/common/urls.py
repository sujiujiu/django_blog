# -*- coding: utf-8 -*-
from django.conf.urls import url,include
import views

urlpatterns = [
    url(r'^graph_captcha/',views.graph_captcha,name='graph_captcha'),
    url(r'^sms_captcha/',views.sms_captcha,name='sms_captcha'),
    url(r'^qiniu_token/',views.qiniu_token,name='qiniu_token'),
]