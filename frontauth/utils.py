# -*- coding: utf-8 -*-
from models import FrontUserModel
import configs

def login(request,email,password):
	user = FrontUserModel.objects.filter(email=email).first()
	if user:
		result = user.check_password(password)
		if result:
			request.session[configs.LOGINED_KEY] = str(user.uid)
			return user
		else:
			return None
	else:
		return None


def logout(request):
	try:
		del request.session[configs.LOGINED_KEY]
	except KeyError:
		pass
