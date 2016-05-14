# -*- coding: utf-8 -*-

from datetime import datetime

from django.core.urlresolvers import reverse

from django.shortcuts import render
from ..models.log_entry import LogEntry

from django.views.generic.base import TemplateView

from ..util import paginate, get_current_group

def log_entries(request):
	entries = LogEntry.objects.all()
	return render(request, 'students/log_entry.html', {'entries': entries})

class LogEntryList(TemplateView):
	template_name = "students/log_entry.html"

	def get_context_data(self, **kwargs):
		context = super(LogEntryList, self).get_context_data(**kwargs)
		entries = LogEntry.objects.all()

		order_by = self.request.GET.get('order_by', '')
		if order_by:
			entries = LogEntry.objects.order_by(order_by)
			reverse = self.request.GET.get('reverse', '')
			if reverse == '1':
				entries = entries.reverse()
		
		paginate_by = 6


		context = paginate(entries, paginate_by, self.request, context, var_name='entries')

		return context

