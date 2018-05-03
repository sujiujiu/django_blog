# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
# from mybbs.models import BlogsPost

def front_index(request):
	return HttpResponse('hh')

def front_login(request):
	pass

def front_regist(request):
	pass