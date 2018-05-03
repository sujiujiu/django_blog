# -*- coding: utf-8 -*-
from django.conf.urls import include, url
import views


urlpatterns = [
    url(r'^$', views.cms_index, name="cms_index"),
    url(r'^login/$', views.cms_login, name="cms_login"),
]
