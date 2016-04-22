#-*- coding: utf-8 -*-

from django.shortcuts import render
from ..models.log_entry import LogEntry

def log_entries(request):
	entries = LogEntry.objects.all()
	return render(request, 'students/log_entry.html', {'entries': entries})
