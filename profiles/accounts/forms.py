from django import forms

# For displaying the hased user password
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# For easy accessiblity of the user model
# Custom or Django's 
from django.contrib.auth import authenticate, get_user_model
from django.core.validators import RegexValidator
from .models import MyUser, Profile
from django.db.models import Q

# For defining a rule for User names
USERNAME_REGEX = '^[a-zA-Z0-9]*$'

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

		"""
		Iniially the account status would be Inactive.
		After the user has confirmed his email, make it active
		"""
		user.is_active = False

		# create a new user hash for activating email
		

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
	"""
	Below code allows only takes the username as
	input and not the email id.
	"""
	# username = forms.CharField(label='UserName', 
	# 							validators=[
	# 							RegexValidator(
	# 								regex = USERNAME_REGEX,
	# 								message = "Username must be alphanumeric",
	# 								code = 'In-Valid Username',
	# 							)]
	# 							)
	
	"""
	For allowing entrace from both email-id and username
	"""
	query = forms.CharField(label='Username/Email')
	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	"""
	We also need to compare the users' accounts with their corresponding passwords
	
	For that purpose we use clean methods
	"""

	def clean(self, *args, **kwargs):
		query= self.cleaned_data.get('query')
		password = self.cleaned_data.get('password')

		"""
		The below commands look up the database twice.
		Once for looking up the username and another for
		looking up the email. We need to optimise that into
		a single lookup.
		"""
		# user_qs1 = User.objects.filter(username__iexact=query)
		# user_qs2 = User.objects.filter(email__iexact=query)
		# user_qs_final = (user_qs1 | user_qs2 ).distinct()
		"""
		Q lookup to rescue. ~~ Above code
		"""
		user_qs_final = User.objects.filter(
				Q(username__iexact=query)|
				Q(email__iexact=query)
			).distinct()

		# check whether the user exists and it's just one query
		if not user_qs_final.exists() and user_qs_final !=1:
			raise forms.ValidationError("InValid Credentials")
		"""
		Most recommended way.
		"""
		# When only looking for the username
		# user_obj = User.objects.filter(username=query).first()
		
		# When looking for the email/username
		user_obj = user_qs_final.first()
		
		# check password of the user
		if not user_obj.check_password(password):
			raise forms.ValidationError("Invalid Credentials -- Invalid Password")
		if not user.is_active:
			raise forms.ValidationError("Inactive User")
		self.cleaned_data['user_obj'] = user_obj
		return super(UserLoginForm, self).clean(*args, **kwargs)

		"""
		Another way of authenticating the user, using: authenticate
		"""
		# the_user = authenticate(username=username, password=password)
		# if not the_user:
		# 	raise forms.ValidationError("Invalid Credentials")
		# return super(UserLoginForm, self).clean(*args, **kwargs)
		"""
		above method is not recommended as it can't be used for
		email/username field being used interchangbly
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


"""
In the above code
	query = User.objects.filter(username__iexact=username)

	the __iexact looks for the exact username value, 
	including the same camelcase.

	Without the __iexact syntax, 
	hasime would be equivalent to HaSiMe, which isn't desirable. 
"""