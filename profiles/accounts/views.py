# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from forms import UserCreationForm, UserLoginForm

from django.contrib.auth import login, get_user_model

User = get_user_model()

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

# Custom UserModel based LogIn and Registration
def register(request, *args, **kwargs):

	form = UserCreationForm(request.POST or None)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/login")
	return render(request, "accounts/register.html", {"form":form})

# It can't be "login" as django.contrib.auth has a module named login. 
# So "userlogin"
def userlogin(request, *args, **kwargs):
	form = UserLoginForm(request.POST or None)

	if form.is_valid():
		username_ = form.cleaned_data.get('username')
		user_obj = User.objects.get(username__iexact=username_)
		login(request, user_obj)
		return HttpResponseRedirect("/")
	return render(request, "accounts/login.html", {'form': form,})