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

from contact_form.forms import ContactForm

import logging

from ..signals import contact_admin_signal
from ..util import get_custom_language

class CustomContactForm(ContactForm):
    """docstring for CustomContactForm"""
    
    def __init__(self, request, *args, **kwargs):
        #call original initializator
        super(CustomContactForm, self).__init__(request=request, *args, **kwargs)

        #this helper object allows us to customize form
        self.helper = FormHelper()

        #form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('contact_admin')

        #twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        #form buttons
        self.helper.add_input(Submit('send_button', _(u'Send')))

    email = forms.EmailField(
        label=_(u"Your email address"))
    
    name = forms.CharField(
        label=_(u"Your name"),
        max_length=128)
    
    body = forms.CharField(
        label=_(u"Your message"),
        max_length=2560,
        widget=forms.Textarea)
   
class ContactView(FormView):
    """docstring for ContactView"""
    template_name = 'contact_form/contact_form.html'
    form_class = CustomContactForm
    success_url = '/contact-admin/'

    def dispatch(self, request, *args, **kwargs):
        get_custom_language(request)
        return super(ContactView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            form.save()
            # raise Exception()
        except Exception as e:
            message = _(u'During sending mail appeared unexpected error. Try send later.') + str(e)
            messages.error(self.request, message)
            logger = logging.getLogger(__name__)
            logger.exception(message)
        else:
            messages.success(self.request, _(u'Message sent successfully!'))
            logger = logging.getLogger(__name__)
            logger.info(_(u'Message to admin was sent success!'))
            contact_admin_signal.send(sender=self.__class__)
        return super(ContactView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ContactView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    # def get_success_url(self):
    #     return reverse('contact_admin')



def contact_admin(request):
    get_custom_language(request)
    #check if form was posted
    if request.method == 'POST':
        #create a form instance and populate  it with data from the request
        form = CustomContactForm(request, request.POST)

        #check whether user data is valid
        if form.is_valid():
            #send email
            try:
                form.save()
            except Exception as e:
                messages.error(request, _(u'During sending mail appeared unexpected error. Try send later.') + str(e))
            else:
                messages.success(request, _(u'Message sent successfully!'))

            #redirect to same contact page with success message
            return HttpResponseRedirect(reverse('contact_admin'))
    #if there was not POST render blank form
    else:
        form = CustomContactForm(request)

    return render(request, 'contact_form/contact_form.html', {'form': form})
