# -*- coding: utf-8 -*-
from django.conf.urls import url,include
import views

urlpatterns = [
    url(r'^captcha/',views.captcha,name='common_captcha'),
]