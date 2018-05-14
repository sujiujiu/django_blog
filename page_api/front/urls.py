# -*- coding: utf-8 -*-
from django.conf.urls import include, url
import views


urlpatterns = [
    url(r'^$', views.front_index, name="front_index"),
    url(r'^login/$', views.front_login, name="front_login"),
    url(r'^regist/$', views.front_regist, name="front_regist"),
    url(r'^logout/$', views.front_logout, name="front_logout"),
    url(r'^sms_captcha/$', views.sms_captcha, name="sms_captcha"),
    # url(r'^article_list/(?P<category_id>\d+)/(?P<page>\d+)/$',views.article_list,name='front_article_list'),
    # url(r'^article_detail/(?P<article_id>[\w\-]+)/$',views.article_detail,name='front_article_detail'),
    # url(r'^forget_password/$',views.forget_password,name='front_forget_password'),
    # url(r'^reset_password/(?P<code>\w+)$',views.reset_password,name='front_reset_password'),
    # url(r'^check_email/(?P<code>\w+)/$',views.check_email,name='front_check_email'),
    # url(r'^comment/$',views.comment,name='front_comment'),
]