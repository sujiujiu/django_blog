# -*-coding:utf-8-*-
from django.conf.urls import url,include
from django.contrib import admin
# 在同目录下的urls.py里需要from xx导入，其他不需要，只需要import views
from myblog import views

urlpatterns = [
    url(r'', include('page_api.front.urls')),
    url(r'^cms/', include('page_api.cms.urls')),
    url(r'^common/', include('page_api.common.urls')), 
]
