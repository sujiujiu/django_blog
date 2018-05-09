# -*- coding: utf-8 -*-
from django.conf.urls import url,include
import views

urlpatterns = [
	url(r'^add_user/$',views.add_user),
	url(r'^front_login/$',views.front_login),
	url(r'^front_logout/$',views.front_logout),
	url(r'^check_login/$',views.check_login),
	url(r'^decorator_check/$',views.decorator_check),
	url(r'^middleware_test/$',views.middleware_test),
]