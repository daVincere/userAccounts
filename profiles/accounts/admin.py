# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import MyUser, MyUserManager, Profile

class UserAdmin(BaseUserAdmin):
	# The forms to add and change user instances
	form = UserChangeForm
	add_form = UserCreationForm

	"""
	The fields to be used in the User Model
	These override the definations on the base UserAdmin
	that reference specific fields on auth.User
	"""

	list_display = ['username', 'email','is_admin']
	list_filter = ['is_admin',]

	fieldsets = [
	(
		None, 
		{'fields': ('username','email', 'password')}
	),
	(
		'Personal Info', {'fields':('zipcode',)}
	),
	(
		'Permissions', 
		{'fields':('is_admin',)}
	),
	]

	# no fucking idea what's happening after this

	# add_fieldsets is not a standard ModelAdmin attribute.
	# UserAdmin overrides get_fieldsets to use this attribute
	# when creating a user

	add_fieldsets = (
		(
			None, 
			{'classes': ('wide',),
			'fields': ('username','email', 'password1', 'password2')}
		),
		)
	search_fields = ('username','email',)
	ordering = ('username','email',)
	filter_horizontal = ()

# Register the new UserAdmin
admin.site.register(MyUser, UserAdmin)

"""
as we are not using django's built in permisions,
unregister the Group model from admin

No idea why! but ...
"""
admin.site.unregister(Group)


admin.site.register(Profile)