from django.shortcuts import render
from django import forms
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic.edit import FormView
from django.utils.translation import ugettext_lazy as _

from studDb.settings import ADMIN_EMAIL

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ContactForm(forms.Form):
	"""docstring for ContactForm"""
	
	def __init__(self, *args, **kwargs):
		#call original initializator
		super(ContactForm, self).__init__(*args, **kwargs)

		#this helper object allows us to customize form
		self.helper = FormHelper()

		#form tag attributes
		self.helper.form_class = 'form-horizontal'
		self.helper.form_method = 'post'
		self.helper.form_action = reverse('contact2')

		#twitter bootstrap styles
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'

		#form buttons
		self.helper.add_input(Submit('send_button', _(u'Send')))
		
	form_email = forms.EmailField(
		label=_(u"Your email address"))
	
	subject = forms.CharField(
		label=_(u"email's subject"),
		max_length=128)
	
	message = forms.CharField(
		label=_(u"Text of message"),
		max_length=2560,
		widget=forms.Textarea)

class ContactView2(FormView):
	"""docstring for ContactView2"""
	
	template_name = 'contact_admin/form.html'
	form_class = ContactForm
	success_url = '/contact2/'

	def dispatch(self, request, *args, **kwargs):
		return super(ContactView2, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		#send email
		subject = form.cleaned_data['subject']
		message = form.cleaned_data['message']
		form_email = form.cleaned_data['form_email']
		try:
			send_mail(subject, message, form_email, [ADMIN_EMAIL])
		except Exception as e:
			msg = _(u'During sending mail appeared unexpected error. Try send later.') + str(e)
			messages.error(self.request, msg)
		else:
			messages.success(self.request, _(u'Message sent successfully!'))
		return super(ContactView2, self).form_valid(form)
		

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
				msg = _(u'During sending mail appeared unexpected error. Try send later.') + str(e)
				messages.error(self.request, msg)
			else:
				messages.success(self.request, _(u'Message sent successfully!'))

			#redirect to same contact page with success message
			return HttpResponseRedirect(reverse('contact2'))
	#if there was not POST render blank form
	else:
		form = ContactForm()

	return render(request, 'contact_admin/form.html', {'form': form})
