# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from ..models.Visiting import Visiting

def journal_list(request):
	journal = Visiting.objects.all()
	return render(request, 'students/journal_list.html', {'journal': journal,})
