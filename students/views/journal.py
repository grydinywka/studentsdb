# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

def journal_list(request):
	students = (
		{'student_name': u'Подоба Віталій'},
		 # 'Mon': u'Пн',
		 # 'Tue': u'Вт',
		 # 'Wed': u'Ср',
		 # 'Thu': u'Чт',
		 # 'Fri': u'Пт',
		 # 'Sat': u'Сб',
		 # 'Sun': u'Нд'},
		{'student_name': u'Корост Андрій'},
		{'student_name': u'Притула Тарас'},
	)
	week = (u'Пн', u'Вт', u'Ср', u'Чт', u'Пт', u'Сб', u'Нд',)

	# return HttpResponse('<h1>Here will be journal of students!</h1>')
	return render(request, 'students/visiting.html', {'students': students, 'xrange': xrange(31), 'week': week})