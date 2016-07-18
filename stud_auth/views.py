from django.shortcuts import render
from django.contrib.auth.views import login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

def custom_login(request):
	if request.user.is_authenticated():
		messages.info(request, _(u"You are already authenticated"))
		return HttpResponseRedirect(reverse('home'))
	else:
		return login(request)