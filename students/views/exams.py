# -*- coding: utf-8 -*-

from datetime import datetime

from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse

from ..models.Exam import Exam
from ..models.Group import Group
from ..models.Student import Student

from django.views.generic import UpdateView, CreateView, DeleteView

class ExamEdit(forms.ModelForm):
	class Meta:
		model = Exam

	title = forms.CharField(
		label = u'Назва іспиту*',
		error_messages = {'required': u'ПОЛЕ НАЗВИ Є ОБОВ’ЯЗКОВЕ'},
		help_text = u'Введіть назву іспиту'
		)

	exam_date = forms.DateField(
		label = u'Дата і час*',
		help_text = u'формат РРРР-ММ-ДД ГГ:ХХ',
		error_messages = {'required': u'ПОЛЕ дати повинно бути присутнім!!!',
						  'initial': u'Формат неправильний'}
		)

	presenter = forms.CharField(
		label = u'Екзаменатор*',
		error_messages = {'required': u'Поле екзаменатора є обов’язковим!'},
		help_text = u'Ім’я та По-батькові'
		)

	exam_group = forms.ModelChoiceField(
		required = False,
		label = u'Груп -а/-и',
		help_text = u'Затисніть клавішу "Control", або "Command" на Маку, щоб обрати більше однієї опції.',
		queryset=Group.objects.all().order_by('title'),
		error_messages = {'invalid_choice': u'Неправильна група'}
		)

	notes = forms.CharField(
		label=u"Нотатки",
		help_text=u"Додаткова інформація",
		required=False,
		max_length=1000
		)

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

def exams_edit_handle(request, eid):
	# return HttpResponse('<h1>Edit exam %s</h1>' % eid)

	exam = Exam.objects.filter(pk=eid)[0]
	
	if request.method == 'POST':
		if request.POST.get('edit_button') is not None:
			errors = {}
			data = {'notes': request.POST.get('notes', '').strip()}
			data_exam_group = []

			title = request.POST.get('title', '').strip()
			if not title:
				errors['title'] = u'Поле назви є обов’язковим'
			else:
				data['title'] = title

			exam_date = request.POST.get('exam_date', '').strip()
			if not exam_date:
				errors['exam_date'] = u'Поле дати і часу іспиту є обов’язковим!'
			else:
				try:
					datetime.strptime(exam_date, '%Y-%m-%d %H:%M')
				except Exception as e:
					errors['exam_date'] = u'Неправильний формат дати і часу: ' + str(e)
				else:
					data['exam_date'] = exam_date
			
			presenter = request.POST.get('presenter', '').strip()
			if not presenter:
				errors['presenter'] = u'Екзаменатор є обов’язковим!'
			else:
				data['presenter'] = presenter

			exam_group = request.POST.getlist('exam_group', '')
			if exam_group:
				for gid in exam_group:
					group = Group.objects.filter(pk=gid)[0]
					data_exam_group.append(group)

			if not errors:
				exam.title = data['title']
				exam.exam_date = data['exam_date']
				exam.presenter = data['presenter']
				exam.notes = data['notes']

				exam.save()
				exam.exam_group.clear()
				for group in data_exam_group:
					exam.exam_group.add(group)

				messages.success(request, u'Іспит %s поредаговано!' % exam)
				return HttpResponseRedirect(reverse('exams'))
			else:
				messages.error(request, u'Виправте наступні помилки')
				return render(request, 'students/exams_edit_handle.html', {'groups': Group.objects.all().order_by('title'),
																		  'errors': errors,
																		  'data_exam_group': data_exam_group,
																		  'eid': eid,
																		  'exam_group': exam_group})
		elif request.POST.get('cancel_button') is not None:
			messages.info(request, u'Редагування іспиту %s відмінено!' % exam)
			return HttpResponseRedirect(reverse("exams"))
	else:
		return render(request, 'students/exams_edit_handle.html', {'exam': exam,
																   'eid': eid,
																   'groups': Group.objects.all().order_by('title')})

def exams_add_handle(request):
	groups = Group.objects.all().order_by('title')

	if request.method == 'POST':
		if request.POST.get('add_button') is not None:
			errors = {}

			data = {'notes': request.POST.get('notes', '').strip()}
			data_exam_group = []

			title = request.POST.get('title', '').strip()
			if not title:
				errors['title'] = u'Назва іспиту є обов’язковою!'
			else:
				data['title'] = title

			exam_date = request.POST.get('exam_date','').strip()
			if not exam_date:
				errors['exam_date'] = u'Дата і час іспиту є обов’язкові!'
			else:
				try:
					datetime.strptime(exam_date, '%Y-%m-%d %H:%M')
				except Exception as e:
					errors['exam_date'] = u'Неправильний формат .' + str(e)
				else:
					data['exam_date'] = exam_date

			presenter = request.POST.get('presenter', '').strip()
			if not presenter:
				errors['presenter'] = u'Екзаменатор є обов’язковим!'
			else:
				data['presenter'] = presenter

			exam_group = request.POST.getlist('exam_group', '')
			
			# id_all_groups = [int(group.id) for group in groups]
			# type_e_g = type(exam_group)

			if exam_group:
				for gid in exam_group:
					group = Group.objects.filter(pk=gid)[0]
					data_exam_group.append(group)

			# if type_e_g is list:
			# 	for group_id in exam_group:
			# 		if not group_id in id_all_groups:
			# 			errors['exam_group'] = u'ПОмилка у виборі групи1'
			# 	if not hasattr(errors, 'exam_group'):
			# 		data['exam_group'] = exam_group
			# else:
			# 	if exam_group in id_all_groups:
			# 		data['exam_group'] = exam_group
			# 	else:
			# 		errors['exam_group'] = u'ПОмилка у виборі групи2'

			if not errors:
				exam = Exam(**data)
				exam.save()
				for group in data_exam_group:
					exam.exam_group.add(group)

				messages.success(request, u'Іспит додано!')
				return HttpResponseRedirect(reverse('exams'))
			else:
				messages.error(request, u'Виправте наступні помилки')
				return render(request, 'students/exams_add_handle.html', {'groups': Group.objects.all().order_by('title'),
																		  'errors': errors,
																		  'e_g': exam_group,
																		  'data': data,
																		  'data_exam_group': data_exam_group,
																		  'students': Student.objects.all()})

		elif request.POST.get('cancel_button') is not None:
			messages.info(request, u'Відмінено створення іспиту!')
			return HttpResponseRedirect(reverse("exams"))
	else:
		return render(request, 'students/exams_add_handle.html', {'groups': groups,
																  'students': Student.objects.all()})

def exams_confirm_delete_handle(request, eid):
	exam = Exam.objects.filter(pk=eid)[0]

	if request.method == 'POST':
		if request.POST.get('cancel_button') is not None:
			messages.info(request, u'Видалення іспиту %s відмінено!' % exam)
			return HttpResponseRedirect(reverse('exams'))
		elif request.POST.get('delete_button') is not None:
			messages.success(request, u'Іспит %s видалено!' % exam)
			exam.delete()
			return HttpResponseRedirect(reverse('exams'))
	else:
		return render(request, 'students/exams_confirm_delete_handle.html', {'eid': eid,
																			 'exam': exam})

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
