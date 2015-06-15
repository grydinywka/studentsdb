# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse

from ..models.Exam import Exam
from ..models.Group import Group

from django.views.generic import UpdateView, CreateView, DeleteView

def exams_list(request):
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

	return render(request, 'students/exams_list.html', {'exams': exams,
													   'valPage': valPage,
													   'listOfPage': listOfPage})

def exams_edit(request, pk):
	return HttpResponse('<h1>Edit exam %s</h1>' % pk)

def exams_add(request):
	return HttpResponse('<h1>Add exam!</h1>')

class ExamEditView(UpdateView):
	model = Exam
	template_name = 'students/exams_edit.html'

	def get_success_url(self):
		messages.success(self.request, u'Іспит %s усішно поредаговано!' % self.object)
		return reverse('exams')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(request, u'Редагування іспиту %s відмінено!' % self.get_object())
			return HttpResponseRedirect(reverse('exams'))
		else:
			return super(ExamEditView, self).post(request, *args, **kwargs)

class ExamAddView(CreateView):
	model = Exam
	template_name = 'students/exams_add.html'

	def get_success_url(self):
		messages.success(self.request, u'Іспит %s створено!' % self.object)
		return reverse('exams')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(request, u'Створення іспиту відмінено!')
			return HttpResponseRedirect(reverse('exams'))
		else:
			return super(ExamAddView, self).post(request, *args, **kwargs)

class ExamDeleteView(DeleteView):
	model = Exam
	template_name = 'students/exams_confirm_delete.html'
	pk_url_kwarg = 'eid'

	def get_success_url(self):
		# messages.success(self.request, u'Іспит %s видалено!' % self.object)
		return reverse('exams')

	def post(self, request, *args, **kwargs):
		if request.POST.get("delete_button"):
			messages.success(request, "Іспит %s був видалений!" % self.get_object())
			self.get_object().delete()
		elif request.POST.get("cancel_button"):
			messages.info(request, "Видалення іспиту %s скасовано!" % self.get_object())
		
		return HttpResponseRedirect(reverse('exams'))
