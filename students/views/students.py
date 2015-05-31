# -*- coding: utf-8 -*-

from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from ..models.Student import Student
from ..models.Group import Group
from ..models.Visiting import Visiting

from datetime import datetime
from PIL import Image

# import sys
# sys.path.append('/data/work/virtualenvs/studDb/src/studDb/studDb/')
from studDb.settings import SIZE_LIMIT_FILE

from django.views.generic import ListView, UpdateView
from django.views.generic.edit import FormView

class isNotImageError(Exception): pass
class tooBigPhotoError(Exception): pass

class StudentList(ListView):
	"""docstring for StudentList"""
	model = Student
	# queryset = Student.objects.all()
	template_name = 'students/studentlistTmp.html'
	context_object_name = 'students'
	# template = 'students/student_class_based_view_template'
	paginate_by = 5

	# def get_context_object_name(self, obj):
	# 	return 'studs'

	def get_context_data(self, **kwargs):
		"""This method adds extra variables to template"""
		#get original context data from parent class
		context = super(StudentList, self).get_context_data(**kwargs)

		#tell template not to show logo on a page
		context['show_logo'] = False
		context['group_list'] = Group.objects.all()

		#return context mapping
		return context

	def get_object(self):
		# Call the superclass
		obj = super(StudentList, self).get_object()
		# Record the last accessed date
		obj.last_accessed = 'timezone.now()'
		obj.save()
		# Return the object
		return obj
	
	def get_queryset(self):
		"""Order students by last name."""
		#get original query set
		qs = super(StudentList, self).get_queryset()

		return qs.order_by('last_name')

class StudentUpdateView(UpdateView):
	"""docstring for StudentUpdateView"""
	
	model = Student
	template_name = 'students/students_edit.html'
	pk_url_kwarg = 'sid'

	def __init__(self, *args, **kwargs):
		super(StudentUpdateView, self).__init__(*args, **kwargs)

		#define additional context
		self.errors = {}
	
	def get_success_url(self):
		messages.success(self.request, u'Студента успішно збережено!')
		return reverse('home')

	def get_context_data(self, **kwargs):
		"""This method adds extra variables to template"""
		#get original context data from parent class
		context = super(StudentUpdateView, self).get_context_data(**kwargs)
		
		if self.errors:
			context['errors'] = None
			# context['errors'] = self.errors
		#return context mapping
		return context

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(self.request, u'Редагування студента відмінено!')
			return HttpResponseRedirect(reverse('home'))
		else:
			last_name = request.POST.get('last_name', '').strip()
			if not last_name:
				self.errors['last_name'] = u"Прізвище є обов’язковим"
				messages.error(self.request, u'Прізвище є обов’язковим!')
			return super(StudentUpdateView, self).post(request, *args, **kwargs)

# Class form for edit students
class StudentEditForm(forms.Form):
	"""docstring for StudentEditForm"""
	first_name = forms.CharField(
		label='First_name',
		max_length=100)

class StudentEditView(FormView):
	"""docstring for StudentEditView"""
	
	template_name = 'students/students_edit.html'
	pk_url_kwarg = 'sid'
	form_class = StudentEditForm
	success_url = '/'

	def form_valid(self, form):
		first_name = form.cleaned_form['first_name']
		try:
			pass
		except Exception as e:
			messages.error(self.request, u'Під час редагування студента виникла ' \
			u'помилка. Спробуйте скористатись даною формою пізніше. ' \
			+ str(e))
		else:
			messages.success(self.request, u'Редагування успішне!')
		return super(StudentEditView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		"""This method adds extra variables to template"""
		#get original context data from parent class
		context = super(StudentEditView, self).get_context_data(**kwargs)
		

		context['object'] = {'id': 1}
		
		#return context mapping
		return context

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(self.request, u'Редагування студента відмінено!')
			return HttpResponseRedirect(reverse('home'))
		else:
			first_name = request.POST.get('first_name', '').strip()
			if not first_name:
				messages.error(self.request, u'Прізвище є обов’язковим!')
			return super(StudentEditView, self).post(request, *args, **kwargs)
		


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
	#Якщо форма була запущена
	if request.method == "POST":
		
		#Якщо кнопка Додати була натиснута:
		if request.POST.get('add_button') is not None:
			
			#Перевіряємо дані на коректність та збираємо помилки
			# TODO: validate input from user
			errors = {}

			# validate student data will go here
			data = {'middle_name': request.POST.get('middle_name'),
					'notes': request.POST.get('notes'),
					'student_journal': request.POST.get('student_journal')}

			#validate user input
			first_name = request.POST.get('first_name', '').strip()
			if not first_name:
				errors['first_name'] = u"Ім’я є обов’язковим"
			else:
				data['first_name'] = first_name

			last_name = request.POST.get('last_name', '').strip()
			if not last_name:
				errors['last_name'] = u"Прізвище є обов’язковим"
			else:
				data['last_name'] = last_name
			
			birthday = request.POST.get('birthday', '').strip()
			if not birthday:
				errors['birthday'] = u"Дата народження є обов’язковою"
			else:
				try:
					datetime.strptime(birthday, '%Y-%m-%d')
				except Exception:
					errors['birthday'] = u"Введіть коректний формат дати (напр. 1984-12-30)"
				else:
					data['birthday'] = birthday
			
			ticket = request.POST.get('ticket', '').strip()
			if not ticket:
				errors['ticket'] = u"Номер білета є обов’язковим"
			else:
				data['ticket'] = ticket
			
			student_group = request.POST.get('student_group', '').strip()
			if not student_group:
				errors['student_group'] = u"Оберіть групу для студента"
			else:
				groups = Group.objects.filter(pk=student_group)
				if len(groups) != 1:
					errors['student_group'] = u"Оберіть коректну групу"
				else:
					data['student_group'] = groups[0]

			study_start = request.POST.get('study_start', '').strip()
			if not study_start:
				errors['study_start'] = u"Поле Початок навчання обов’язкове"
			else:
				try:
					datetime.strptime(study_start, '%Y-%m-%d')
				except Exception:
					errors['study_start'] = u"Введіть коректний формат дати (напр. 2014-09-01)"
				else:
					data['study_start'] = study_start

			#validate image
			try:
				photo = request.FILES.get('photo')
				img = Image.open(photo)
				sizePhoto = photo.size
				if not Image.isImageType(img):
					raise isNotImageError()
				if sizePhoto > SIZE_LIMIT_FILE:
					raise tooBigPhotoError()
			except IOError:
				errors['photo'] = u"Помилка при відкритті фото"
			except AttributeError:
				pass
			except isNotImageError:
				errors['photo'] = u"Це не зображення"
			except tooBigPhotoError:
				errors['photo'] = u"Розмір фото не може перевищувати " + str(SIZE_LIMIT_FILE) + u" байт.\
									Додиний файл містить " + str(sizePhoto) + u" байт"
			else:
				data['photo'] = photo
			
			#Якщо дані були введені коректно:
			if not errors:
				#Створюємо та зберігаємо студента в базу
				# student = Student(
				# 	first_name=request.POST['first_name'],
				# 	last_name=request.POST['last_name'],
				# 	middle_name=request.POST['middle_name'],
				# 	birthday=request.POST['birthday'],
				# 	ticket=request.POST['ticket'],
				# 	student_group=Group.objects.get(pk=request.POST['student_group']),
				# 	study_start=request.POST['study_start'],
				# 	photo=request.FILES['photo'],)
				
				student = Student(**data)
				student.save()
				
				messages.success(request, u"Студента %s успішно додано!" % student)
				#Повертаємо користувача до списку студентів
				return HttpResponseRedirect(reverse('home'))
			
			#Якщо дані були введені некоректно:
			else:
				messages.warning(request, u"Будь-ласка, виправте наступні помилки!")
				#Віддаємо шаблон форми разом із знайденими помилками
				return render(request, 'students/students_add.html',
					{'groups': Group.objects.all().order_by('title'),
					 'errors': errors})
		#Якщо кнопка Скасувати була натиснута:
		elif request.POST.get('cancel_button') is not None:
			messages.info(request, u"Додавання студента скасовано!")
			#Повертаємо користувача до списку студентів
			return HttpResponseRedirect(reverse('home'))
	#Якщо форма не була запущена:
	else:
		#Повертаємо код початкового стану форми
		return render(request, 'students/students_add.html',
			{'groups': Group.objects.all().order_by('title')})

def students_edit(request, sid):
	student = Student.objects.filter(pk=sid)[0]
	#if form was posted
	if request.method == 'POST':
		#if edit_button was pushed
		if request.POST.get('edit_button') is not None:
			#TODO: validate input from user
			errors = {}

			if not errors:
				student.first_name = request.POST.get('firstName', '').strip()
				student.last_name = request.POST.get('lastName', '').strip()
				student.middle_name = request.POST.get('middleName', '').strip()
				student.birthday = request.POST.get('birthday', '').strip()
				student.ticket = request.POST.get('ticket', '').strip()
				
				actWithPhoto = request.POST.get('pho', '')
				if actWithPhoto == 'change':
					student.photo = request.FILES.get('photo')
				elif actWithPhoto == 'delete':
					student.photo = None
				student.notes = request.POST.get('notes', '').strip()
				student.study_start = request.POST.get('study_start', '').strip()
				student_group = request.POST.get('student_group', '').strip()
				student.student_group = Group.objects.get(pk=student_group)
				student_journal = request.POST.get('journal', '').strip()
				if student_journal == '':
					student.student_journal = None
				else:
					student.student_journal = Visiting.objects.get(pk=student_journal)

				student.save()
				#returns user to list of students
				return HttpResponseRedirect(reverse('home'))
			else:
				return render(request, 'students/students_edit.html',
					{'groups': Group.objects.all().order_by('title'),
					 'journals': Visiting.objects.all().order_by('title'),
					 'errors': errors,
					 'sid': sid,
					 'student': student,
					 'actWithPhoto': "actWithPhoto"})
		#if cancel_button was pushed
		elif request.POST.get('cancel_button') is not None:
			return HttpResponseRedirect(reverse('home'))	
	#is form wasn't posted
	else:
		#give code of begin state
		return render(request, 'students/students_edit.html',
			{'sid': sid,
			 'student': student,
			 'groups': Group.objects.all().order_by('title'),
			 'journals': Visiting.objects.all().order_by('title')
			})

def students_delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' % sid)
