# -*- coding: utf-8 -*-
from functools import wraps

from models import FrontUserModel
import configs
from django.shortcuts import redirect,reverse

def front_login_required(func):
	@wraps(func)
	def wrapper(request,*args,**kwargs):
		user_id = request.session.get(configs.LOGINED_KEY)
		if user_id:
			return func(request,*args,**kwargs)
		else:
			# 如果session中不存在uid，说明没有登录
			# 如果用户没有登录，跳转到登录页面，并且需要添加一个next的url到url中
			url = reverse('front_login') + '?next=' + request.path
			return redirect(url)
	return wrapper


