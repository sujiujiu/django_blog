# -*- coding: utf-8 -*-
from django.conf.urls import include, url
import views


urlpatterns = [
    url(r'^$', views.front_index, name="front_index"),
    url(r'^login/$', views.front_login, name="front_login"),
    url(r'^regist/$', views.front_regist, name="front_regist"),
]