# -*- coding: utf-8 -*-
import hashlib
import configs

def make_password(raw_password,salt=None):
	if not salt:
		salt = configs.PASSWORD_SALT

	hash_password = hashlib.md5(salt+raw_password).hexdigest()
	return hash_password


def check_password(raw_password,hash_password):
	# 首先需要对raw_password进行加密,
	# 而且使用的salt必须一样，然后再和数据库中的密码进行对比。
	if not raw_password:
		return False

	tmp_password = make_password(raw_password)
	if tmp_password == hash_password:
		return True
	else:
		return False