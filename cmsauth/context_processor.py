# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from models import CmsUserModel


# 把CmsUser的avatar属性添加到user当中
# 在view.py中可以通过user.avatar的方式调用，
# 类似在前台为了获得user的front.user一样，需要上下文处理器
# 查询集做跨表查询时，QuerySet可以使用双下划线“__”
def CmsContextProcessor(request):
	user = request.user
	if not hasattr(user,'avatar'):
		cmsuser = CmsUserModel.objects.filter(user__pk=user.pk).first()
		if cmsuser:
			setattr(user,'avatar',cmsuser.avatar)
	return {'user':user}
