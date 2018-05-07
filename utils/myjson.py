# -*- coding: utf-8 -*-
from django.http import JsonResponse
from collections import namedtuple


class HttpCode(object):
	"""http状态码:
		200: 请求正常(ok)
		400: 请求参数错误(paramserror)
		401: 没有权限访问(unauth)
		405: 请求方法错误(methoderror)
		500：服务器错误(servererror)
	"""
    ok = 200
    paramserror = 400
    unauth = 401
    methoderror = 405
    servererror = 500

# 请求正常的json返回函数
def json_result(code=httpcode.ok,message='',data={},kwargs={}):
	json = {'code':code,'message':message,'data':data}
	if kwargs.keys():
		# 把json和kwargs合并成一个字典
		for k,v in kwargs.items():
			json[k] = v
	return JsonResponse(json)

def json_params_error(message=''):
	"""
		请求参数错误
	"""
	return json_result(code=httpcode.paramserror,message=message)

def json_unauth_error(message=''):
	"""
		没有权限访问
	"""
	return json_result(code=httpcode.unauth,message=message)

def json_method_error(message=''):
	"""
		请求方法错误
	"""
	return json_result(code=httpcode.methoderror,message=message)


def json_server_error(message=''):
    """
        服务器内部错误
    """
    return json_result(code=HttpCode.servererror, message=message or '服务器内部错误！')