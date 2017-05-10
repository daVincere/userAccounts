from django import forms

# For displaying the hased user password
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# For easy accessiblity of the user model
# Custom or Django's 
from django.contrib.auth import authenticate, get_user_model
from django.core.validators import RegexValidator
from .models import MyUser, Profile

# For defining a rule for User names
USERNAME_REGEX = '^[a-zA-Z0-9@+-]*$'

User = get_user_model()

class UserCreationForm(forms.ModelForm):
	"""
	A form for creating new users.
	Includes all the required fields, plus a repeated password

	We are customising the whole thing 
	"""
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username','email',)

	# role of this function??
	def clean_password2(self):
		# check that the two password entries meet
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 !=password2:
			raise forms.ValidationError("Passwords don't match")
		return password2


	def save(self, commit=True):
		# save the provided password in hashed format
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])

		if commit:
			user.save()
		return user

class UserChangeForm(forms.ModelForm):
	"""
	A form for updating users. Includes all the fields
	on the user, but replaces the password field with 
	admin's password hash display field
	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ['username','email', 'password', 'is_staff' ,'is_active', 'is_admin']


	def clean_password(self):
		# no fucking idea why!!

		return self.initial["password"]

# For getting the user Logged In
class UserLoginForm(forms.Form):
	username = forms.CharField(label='UserName', 
								validators=[
								RegexValidator(
									regex = USERNAME_REGEX,
									message = "Username must be alphanumeric",
									code = 'In-Valid Username',
								)]
								)

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	"""
	We also need to compare the users' accounts with their corresponding passwords
	
	For that purpose we use clean methods
	"""

	def clean(self):
		username= self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		
		"""
		Most recommended way.
		"""
		user_obj = User.objects.filter(username=username).first()
		# check the username
		if not user_obj:
			raise forms.ValidationError("Invalid Credentials -- Invalid Username") 
		# check password of the user
		else:
			if not user_obj.check_password(password):
				raise forms.ValidationError("Invalid Credentials -- Invalid Password")
		# return super(UserLoginForm, self).clean(*args, **kwargs)

		"""
		Another way of authenticating the user, using: authenticate
		"""
		# the_user = authenticate(username=username, password=password)
		# if not the_user:
		# 	raise forms.ValidationError("Invalid Credentials")
		# return super(UserLoginForm, self).clean(*args, **kwargs)
		"""
		above method is not recommended.
		"""	

	"""
	One way of doing it, but not recommended
	"""
	# checking if the username even exists
	# def clean_username(self):
	# 	username = self.cleaned_date.get('username')
	# 	user_qs = User.objects.filter(username=username)
	# 	user_exists= user_qs.exists()
	# 	if not user_exists and user_qs.count() !=1:
	# 		raise form.ValidationError("Invalid Credentials")
	# 	return username
