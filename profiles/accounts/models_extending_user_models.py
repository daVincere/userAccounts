# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.conf import settings

from django.db.models.signals import post_save

# extends the usermodel
# any registered user can have a profile
class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	city = models.CharField(max_length=120, null=True, blank=True)

	def __unicode__(self):
		return str(self.user.username)

# To create a profile(defined above), 
# everytime a new user is registered, we use Signals

def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
	# if user model is created
	if created:
		# create the profile
		try:
			Profile.objects.create(user=instance)
		except:
			pass


post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)