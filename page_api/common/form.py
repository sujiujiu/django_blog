# -*- coding: utf-8 -*-
import json
from django import forms
from utils import myjson

class BaseForm(forms.Form):
	def get_error(self):
		errors = self.errors.as_json()
		error_dict = json.loads(errors)
		message = ''
		for k,v in error_dict.items():
			message = v[0].get('message',None)
		return message

	def get_error_response(self):
		if self.errors:
			return myjson.json_params_error(message=self.get_error())
		else:
			return myjson.json_result()