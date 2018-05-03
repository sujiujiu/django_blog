# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from forms import LoginForm

def cms_index(request):
	return render(request, 'cms_index.html')

def cms_login(request):
	if request.method == 'GET':
		return render(request, 'cms_login.html')
	else:
		# 1.获取表单
		# 2.验证表单
		# 3.如果表单存在则获取输入框中的账号密码
		# 4.验证与本地账号密码是否相等，如相等跳转到主页，否则报错
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username',None)
			password = form.cleaned_data.get('password',None)
			if username == 'xiaomin' and password == '123456':
				return redirect(reverse('cms_index'))
			else:
				return render(request,'cms_login.html',{'error':u'用户名或密码错误!'})
				# return render(request,'cms_login.html',{'msg':u'用户名或密码错误!'})
		else:
			return render(request, 'cms_login.html',{'error':form.get_error()})
			



def cms_regist(request):
	pass