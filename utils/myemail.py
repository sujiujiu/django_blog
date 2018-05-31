# -*- coding: utf-8 -*-
import time
import hashlib
import random
import strings
from django.core.cache import cache
from django.shortcuts import reverse
from django.conf import settings
from django.core import mail


def email_captcha():
	# 生成四位随即字母+数字组合
	source = list(string.letters) + list([str(i) for i in xrange(0,10)])
    captcha_list = random.sample(source, 4)
    captcha = ''.join(captcha_list)
    return captcha


def send_email(request,receivers,subject=None,message=None):
	'''
		receivers: 接收的邮箱，
		subject：文件主体（算是title），
		message：发送的内容，
		captcha:发送的验证码

	'''
	# code = hashlib.md(str(time.time())+receivers).hexdigest()

	captcha = email_captcha()
	cache.set(captcha,receivers,120)

	if not subject:
		subject = u'邮箱验证码'
	if not message:
		message = u'请在2分钟内完成注册，验证码2分钟内有效'

	# 发送的邮箱
	from_mail = settings.EMAIL_HOST_USER

	# 如果传入的接收邮箱是字符串，将它转换成数组
	if isinstance(receivers,str) or isinstance(receivers,unicode):
		# 接收的邮箱列表
		recipient_list = [receivers]
	if mail.send_mail(subject,message,from_mail,recipient_list):
		return True
	else:
		return False