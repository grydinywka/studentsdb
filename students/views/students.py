# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.Student import Student

# Views for Students
def students_list(request):
	students = Student.objects.all()
	allStud = len(students)
	valStudOnPage = int(request.GET.get('valstud', 3))
	valPage = allStud/valStudOnPage
	
	if allStud % valStudOnPage != 0:
		valPage += 1
	listOfPage = [str(i) for i in xrange(1, valPage+1, 1)]

	# try to order students list
	order_by = request.GET.get('order_by', '')
	if order_by in ('id', 'last_name', 'first_name', 'ticket'):
		students = students.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			students = students.reverse()
	elif order_by == '':
		students = students.order_by('last_name')

	# my paginator students
	page = request.GET.get('page', '')
	
	try:
		page = int(float(page))
	except ValueError:
		page = 1
	if page > valPage or page < 1:
		page = valPage
	
	large = valStudOnPage*page
	little = large - valStudOnPage
	if allStud > 1:
		students = students[little:large]

	#paginator students
	# paginator = Paginator(students, 3)
	# page = request.GET.get('page')
	# try:
	# 	students = paginator.page(page)
	# except PageNotAnInteger:
	# 	# If page is not an integer, deliver first page.
	# 	students = paginator.page(1)
	# except EmptyPage:
	# 	# If page is out of range (e. g. 9999), deliver
	# 	# last page of results.
	# 	students = paginator.page(paginator.num_pages)

	return render(request, 'students/students_list.html', {'students': students,
														   'valPage': valPage,
														   'listOfPage': listOfPage})
	
	# return HttpResponse('<h1>Hello World!</h1>')

def students_add(request):
	return HttpResponse('<h1>Students Add Form</h1>')

def students_edit(request, sid):
	return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' % sid)
