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
from django.views.generic.base import TemplateView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from ..util import paginate, boundsStuds, get_current_group

class MyModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "My Object #%i" % obj.id

class ExamEdit(forms.ModelForm):
	class Meta:
		model = Exam

	def __init__(self, *args, **kwargs):
		super(ExamEdit, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)
		# if 'id' in args[0]:
		# 	if args[0]['id']:
		pk = args[1].id
		self.helper.form_action = reverse('exams_edit',
			kwargs={'eid': pk})
		# 	else:
		# 		self.helper.form_action = reverse('exams_add')
		# else:
		# 	self.helper.form_action = reverse('exams_edit',
		# 		kwargs={'eid': self.instance)})

		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'

		# set form field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'

		self.helper.layout[-1] = FormActions(
			Submit('edit_button', u'Редагувати', css_class="btn btn-primary"),
			Submit('cancel_button', u'Скасувати', css_class="btn btn-link")
			)

	title = forms.CharField(
		label = u'Назва іспиту*',
		error_messages = {'required': u'ПОЛЕ НАЗВИ Є ОБОВ’ЯЗКОВЕ'},
		help_text = u'Введіть назву іспиту'
		)

	exam_date = forms.DateTimeField(
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

	exam_group = forms.ModelMultipleChoiceField(
		required = False,
		label = u'Груп -а/-и',
		# help_text = u'Затисніть клавішу "Control", або "Command" на Маку, щоб обрати більше однієї опції.',
		queryset=Group.objects.all().order_by('title'),
		error_messages = {'invalid_choice': u'Неправильна група'}
		)

	notes = forms.CharField(
		label=u"Нотатки",
		help_text=u"Додаткова інформація",
		required=False,
		max_length=1000
		)

class ExamList(TemplateView):
	template_name = "students/exams_list_for_cbv.html"

	def get_context_data(self, **kwargs):
		context = super(ExamList, self).get_context_data(**kwargs)

		exams = Exam.objects.order_by('title')
		order_by = self.request.GET.get('order_by', '')
		if order_by in ('id', 'title', 'exam_date', 'presenter', 'exam_group'):
			exams = exams.order_by(order_by)
			if self.request.GET.get('reverse', '') == '1':
				exams = exams.reverse()

		current_group = get_current_group(self.request)
		exams1 = []
		if current_group:
			context['current_group'] = current_group
			for exam in exams:
				if current_group in exam.exam_group.all():
					exams1.append(exam)
		else:
			exams1 = exams

		paginate_by = 4
		context = paginate(exams1, paginate_by, self.request, context, var_name='exams')

		return context

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

def exams_edit_django_form(request, eid):
	exam = Exam.objects.filter(pk=eid)[0]
	
	if request.method == 'POST':
		form = ExamEdit(request.POST, exam)
		if request.POST.get('edit_button') is not None:
			data_exam_group = []

			if form.is_valid():
				exam.title = form.cleaned_data['title']
				exam.exam_date = form.cleaned_data['exam_date']
				exam.presenter = form.cleaned_data['presenter']
				exam.exam_group = form.cleaned_data['exam_group']
				exam.notes = form.cleaned_data['notes']

				try:
					exam.save()
				except Exception as e:
					messages.error(request, (u"Невдале редагування %s!" % exam) + str(e))
				else:
					messages.success(request, u"Іспит %s був поредагований успішно!" % exam)

				return HttpResponseRedirect(reverse('exams'))
			else:
				messages.info(request, "Validation errors")
				return render(request, 'students/exams_edit_django_form.html',
					{'eid': eid,
					 'form': form})

		elif request.POST.get('cancel_button') is not None:
			messages.info(request, u'Редагування іспиту %s відмінено!' % exam)
			return HttpResponseRedirect(reverse("exams"))
	else:
		default = {'title': exam.title,
				   'exam_date': exam.exam_date,
				   'presenter': exam.presenter,
				   'exam_group': exam.exam_group.all(),
				   'notes': exam.notes}

		form = ExamEdit(default, exam)
		# form = ExamEdit(initial={
		# 						 "exam_group": exam.exam_group.all(),
		# 						 "title": exam.title,
		# 						 "exam_date": exam.exam_date,
		# 		   				 "presenter": exam.presenter,
		# 		   				 "notes": exam.notes
		# 						 })
		return render(request, 'students/exams_edit_django_form.html',
			{'groups': Group.objects.all().order_by('title'),
			 'eid': eid,
			 'form': form,
			 'default': exam.exam_group
			})

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
	form_class = ExamEdit

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
