# -*- coding: utf-8 -*-

from django.shortcuts import render
from django import forms
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from studDb.settings import ADMIN_EMAIL

class ContactForm(forms.Form):
	"""docstring for ContactForm"""
	
	form_email = forms.EmailField(
		label=u"Ваша Імайл Адреса")
	
	subject = forms.CharField(
		label=u"Заголовок листа",
		max_length=128)
	
	message = forms.CharField(
		label=u"Текст повідомлення",
		max_length=2560,
		widget=forms.Textarea)

def contact_admin(request):
	#check if form was posted
	if request.method == 'POST':
		#create a form instance and populate  it with data from the request
		form = ContactForm(request.POST)

		#check whether user data is valid
		if form.is_valid():
			#send email
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']
			form_email = form.cleaned_data['form_email']
			try:
				send_mail(subject, message, form_email, [ADMIN_EMAIL])
			except Exception as e:
				messages.error(request, u'Під час відправки листа виникла непередбачувана ' \
				u'помилка. Спробуйте скористатись даною формою пізніше. ' \
				+ str(e))
			else:
				messages.success(request, u'Повідомлення успішно надіслане!')

			#redirect to same contact page with success message
			return HttpResponseRedirect(reverse('contact_admin'))
	#if there was not POST render blank form
	else:
		form = ContactForm()

	return render(request, 'contact_admin/form.html', {'form': form})
