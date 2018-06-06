# -*- coding: utf-8 -*-
import configs
from models import FrontUserModel

def auth(request):
	'''全局使用user
	'''
	if request.session.get(configs.LOGINED_KEY):
		if hasattr(request,'front_user'):
			# print request.front_user.username
			return {'front_user':request.front_user}
		else:
			uid = request.session.get(configs.LOGINED_KEY)
			user = FrontUserModel.objects.filter(pk=uid)
			return {'front_user':user}
	else:
		return {}
