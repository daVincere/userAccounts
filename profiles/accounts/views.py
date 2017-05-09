# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
def home(request):
	if request.user.is_authenticated():
		context = {
		'text' : request.user.username
		}
	else:
		context = {
		'text' : 'get a user logged in',
		}
	return render(request, "home.html", context)