# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from forms import CMSLoginForm

@login_required
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
		form = CMSLoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username',None)
			password = form.cleaned_data.get('password',None)
			remember = form.cleaned_data.get('remember',None)
			user = authenticate(username=username,password=password)
			if user:
				login(request, user)
				if remember:
					# 设置None，默认时间是14天
					request.session.set_expiry(None)
				else:
					# 设置为0，意思是浏览器一旦关闭,session就会过期
					request.session.set_expiry(0)
				# 用于退出后重定向
				nexturl = request.GET.get('next')
				if nexturl:
					return redirect(nexturl)
				else:
					return redirect(reverse('cms_index'))
			else:
				return render(request, 'cms_login.html', {'error':u'用户名或密码错误!'})
				# return render(request,'cms_login.html',{'msg':u'用户名或密码错误!'})
		else:
			return render(request, 'cms_login.html', {'error':form.get_error()})
			
# 注销
def cms_logout(request):
	logout(request)
	return redirect(reverse('cms_login'))
