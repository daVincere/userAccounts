from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser
	)
# for adding validators
from django.core.validators import RegexValidator

# for post_save
from django.db.models.signals import post_save
# 
# Model manager
class MyUserManager(BaseUserManager):
	def create_user(self, username, email, password=None):
		"""
		Creates and saves a User with the given email,
		date of birth and password
		"""

		if not email:
			raise ValueError('Users must have an email addess')

		user = self.model(
			username = username,
			email = self.normalize_email(email),
			)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self,username ,email, password):
		"""
		Creates and saves a superuser with the given email, 
		date of birth and password
		"""
		user = self.create_user(
			username,
			email, 
			password=password,
			)

		user.is_admin = True
		user.is_staff = True
		user.save(using=self._db)
		return user

USERNAME_REGEX = '^[a-zA-Z0-9.@+-]*$'
# 
# This is our UserModel, the customised one.
class MyUser(AbstractBaseUser):

	username = models.CharField(
								max_length=120,
								validators=[
									RegexValidator(
										regex=USERNAME_REGEX,
										message='Username must be alphanumeric or contain ".@+-"',
										code='invalid_username'
										)],
								unique=True,
								)

	email = models.EmailField(
							verbose_name='email address',
							max_length=255,
							unique=True,
							)

	zipcode = models.CharField(max_length=120, default='110010')

	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)

	objects = MyUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email',]

	def get_full_name(self):
		# The user is identified by their email email_address
		return self.email

	def get_short_name(self):
		# 
		return self.email

	def __unicode__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		"""
		Does the user have permissions?
			Always
		"""
		return True

	def has_module_perms(self, app_label):
		"""
		Does the user have permissions to view the
		app app_label
		"""
		return True

	"""
	No need to use fancy code. 
	Alternative on line: 67
	"""
	# @property
	# def is_staff(self):
	# 	"""
	# 	IS the user a staff memeber
	# 		Yes, most of the times
	# 	"""
	# 	return self.is_admin


