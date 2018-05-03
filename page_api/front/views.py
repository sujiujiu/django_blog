# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
# from mybbs.models import BlogsPost

def front_index(request):
	return render(request, 'cms_index.html')

def front_login(request):
	pass

def front_regist(request):
	pass