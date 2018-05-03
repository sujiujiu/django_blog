# -*- coding: utf-8 -*-
from django import forms

class FrontLoginForm(forms.Form):
	username = forms.CharField(max_length=10, min_length=4)
	password = forms.CharField(max_length=20, min_length=6)
	remember = forms.BooleanField(required=False)
	captcha = forms.CharField(max_length=4,min_length=4)


class FrontRegistForm(forms.Form):
	telephone = forms.IntegerField(max_length=11, min_length=11)
	cms_captcha = forms.IntegerField(max_length=6, min_length=6)
