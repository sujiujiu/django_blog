# -*- coding: utf-8 -*-
from django import forms

class CMSLoginForm(forms.Form):
	username = forms.CharField(max_length=10, min_length=4)
	password = forms.CharField(max_length=20, min_length=6)
	


