# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from ..models.Exam import Exam

def exam_list(request):
	exams = Exam.objects.all()
	allExam = len(exams)
	valExamOnPage = int(request.GET.get('valExam', 3))
	valPage = allExam/valExamOnPage
	
	if allExam % valExamOnPage != 0:
		valPage += 1
	listOfPage = [str(i) for i in xrange(1, valPage+1, 1)]

	# try to order students list
	order_by = request.GET.get('order_by', '')
	if order_by in ('id', 'title', 'exam_date', 'presenter', 'exam_group'):
		exams = exams.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			exams = exams.reverse()
	elif order_by == '':
		exams = exams.order_by('title')

	# my paginator students
	page = request.GET.get('page', '')
	
	try:
		page = int(float(page))
	except ValueError:
		page = 1
	if page > valPage or page < 1:
		page = valPage
	
	large = valExamOnPage*page
	little = large - valExamOnPage
	if allExam > 1:
		exams = exams[little:large]

	return render(request, 'students/exam_list.html', {'exams': exams,
													   'valPage': valPage,
													   'listOfPage': listOfPage})

def exam_edit(request, gid):
	return HttpResponse('<h1>Edit exam %s</h1>' % gid)
