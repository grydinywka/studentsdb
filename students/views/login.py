from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import FormActions

class LoginAuthForm(forms.ModelForm):
	"""docstring for StudentEditForm"""
	class Meta:
		model = User
		fields = ['username', 'password']
		exclude = ()

	def __init__(self, *args, **kwargs):
		super(LoginAuthForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		# set form tag attributes
		self.helper.form_action = reverse('login')
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal a'

		# set form field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = False
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'
		
		# add buttons
		self.helper.layout[-1] = FormActions(
			Submit('login_button', u'Log In', css_class="btn btn-primary")
			)

	username = forms.CharField(
		label=u'Login',
		max_length=100,
		error_messages={'required': u"Login is required!",
						'unique': 'The error!1!'}
		)

	password = forms.CharField(
		label=u'Password',
		error_messages={'required': u"Password is required!"}
		)

	no_field = forms.CharField(required=False)

def login(request):
	if request.method == 'POST':
		req = request.POST
		form = LoginAuthForm(req)

		if req.get('login_button') is not None:
			data = {}

			data['username'] = req.get('username')
			data['password'] = req.get('password')

			from django.contrib.auth import authenticate
			user = authenticate(username=data['username'], password=data['password'])
			if user is not None:
				# the password verified for the user
				if user.is_active:
					messages.info(request, "User is valid, active and authenticated")
					return HttpResponseRedirect(reverse('home'))
				else:
					messages.info(request, "The password is valid, but the account has been disabled!")
					return render(request, 'students/login.html', {'form': form})
			else:
				# the authentication system was unable to verify the username and password
				messages.info(request, "The username and password were incorrect.")
				return render(request, 'students/login.html', {'form': form})
		
	else:
		form = LoginAuthForm()
		return render(request, 'students/login.html', {'form': form})