# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from forms import UserCreationForm, UserLoginForm

from django.contrib.auth import login, get_user_model, logout

from .models import ActivationProfile
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
		"""
		We are getting the data cleaned in the login form
		No need to do it again.
		"""
		# query = form.cleaned_data.get('query')
		# user_obj = User.objects.get(username__iexact=query)
		"""
		as an alternative
		"""
		user_obj = form.cleaned_data.get('user_obj')
		login(request, user_obj)
		return HttpResponseRedirect("/")
	return render(request, "accounts/login.html", {'form': form,})


def userlogout(request):
	logout(request)
	return HttpResponseRedirect('/login')


def activate_user_view(request, code=None, *args, **kwargs):
	if code:
		act_profile = ActivationProfile.objects.filter(key=code)
		if act_profile_qs.exists() and act_profile_qs.count()==1:
			act_obj = act_profile_qs.first()
			if not act_obj.expired:
				user_obj = act_obj.user
				user_obj.is_active = True
				user_obj.save()
				act_obj.expired = True
				act_obj.save()

				return HttpResponseRedirect("/login")
	return HttpResponseRedirect('/login')