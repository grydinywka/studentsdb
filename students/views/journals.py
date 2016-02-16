# -*- coding: utf-8 -*-

import json

from django.shortcuts import render
from django.http import HttpResponse
from ..models.Visiting import Visiting
from ..models.Group import Group

def journal_list(request):
	journal = Visiting.objects.all()
	return render(request, 'students/journal_list.html', {'journal': journal,})

def data_requests(request):
	if 'HTTP_ACCEPT' in request.META and "application/json" in request.META['HTTP_ACCEPT']:
		content_type = "application/json"
	else:
		content_type = "text/plain"

	new_http_requests = Group.objects.all().order_by('title')
	data = serializers.serialize('json', new_http_requests)

	return HttpResponse(json.dumps(data, ensure_ascii=False), content_type=content_type)