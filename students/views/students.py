# -*- coding: utf-8 -*-

from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.exceptions import ValidationError

from ..models.Student import Student
from ..models.Group import Group
from ..models.Visiting import Visiting

from datetime import datetime
from PIL import Image

# import sys
# sys.path.append('/data/work/virtualenvs/studDb/src/studDb/studDb/')
from studDb.settings import SIZE_LIMIT_FILE

from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

class isNotImageError(Exception): pass
class tooBigPhotoError(Exception): pass
class NoPhotoError(Exception): pass

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
	template_name = 'students/students_edit3.html'
	pk_url_kwarg = 'sid'

	def get_success_url(self):
		messages.success(self.request, u'Студента успішно збережено!')
		return reverse('home')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(self.request, u'Редагування студента відмінено!')
			return HttpResponseRedirect(reverse('home'))
		else:
			return super(StudentUpdateView, self).post(request, *args, **kwargs)


# Class form for edit students
class StudentEditForm(forms.ModelForm):
	"""docstring for StudentEditForm"""
	class Meta:
		model = Student

	def __init__(self, *args, **kwargs):
		super(StudentEditForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		# set form tag attributes
		if 'instance' in kwargs:
			if kwargs['instance']:
				self.helper.form_action = reverse('students_edit',
					kwargs={'sid': kwargs['instance'].id})
			else:
				self.helper.form_action = reverse('students_add')
		else:
			self.helper.form_action = reverse('students_add')
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'

		# set form field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'
		
		# add buttons
		if 'instance' in kwargs:
			if kwargs['instance']:
				self.helper.layout[-1] = FormActions(
					Submit('edit_button', u'Редагувати', css_class="btn btn-primary"),
					Submit('cancel_button', u'Скасувати', css_class="btn btn-link")
					)
			else:
				self.helper.layout[-1] = FormActions(
					Submit('add_button', u'Додати', css_class="btn btn-primary"),
					Submit('cancel_button', u'Скасувати', css_class="btn btn-link")
					)
		else:
			self.helper.layout[-1] = FormActions(
				Submit('add_button', u'Додати', css_class="btn btn-primary"),
				Submit('cancel_button', u'Скасувати', css_class="btn btn-link")
				)
		
	def clean(self, value=None):
		if value is not None:
			groups = Group.objects.filter(leader=value)
			if len(groups) > 0 and self.cleaned_data.get('student_group') != groups[0]:
				raise forms.ValidationError('No name')
		return self.cleaned_data

	first_name = forms.CharField(
		label='Ім’я*',
		initial="Андрій",
		max_length=100,
		help_text=u"Введіть Ваше ім’я",
		error_messages={'required': u"Ім’я є обов’язковим"}
		)

	last_name = forms.CharField(
		label='Прізвище*',
		initial="Коваль",
		help_text=u"Введіть Ваше Прізвище",
		error_messages={'required': u"Прізвище є обов’язковим"}
		)

	middle_name = forms.CharField(
		label='По-батькові',
		required=False
		)

	birthday = forms.DateField(
		label=u"Дата Народження*",
		initial="1970-2-24",
		help_text=u"Ваша дата народження у форматі РРРР-ММ-ДД",
		error_messages={'required': u"Поле дати народження є обов’язковим",
						'initial': u"Ведіть правильний формат Дати"}
		)

	# actWithPhoto = forms.ChoiceField(
	# 	label=u'Дія з Фото*:',
	# 	widget=forms.RadioSelect,
	# 	choices=(('leave', 'Leave',), ('change', 'Edit',), ('drop', 'Delete',),)
	# 	)

	photo = forms.ImageField(
		label=u'Фото',
		help_text=u'Виберіть фото',
		required=False,
		error_messages={'invalid': u'Ваше фото не пройшло валідацію!',
						'required': u'Фото є обов’язковим'}
		)

	ticket = forms.IntegerField(
		label=u'Білет*',
		help_text=u'№ студентського квитка',
		min_value=1,
		max_value=999999,
		error_messages={'min_value': u'Мінімальне значення 1!'}
		)

	notes = forms.CharField(
		label=u'Нотатки',
		help_text=u'Додаткова інформація',
		max_length=2000,
		required=False
		)

	student_group = forms.ModelChoiceField(
		label=u'Група*',
		queryset=Group.objects.all(),
		empty_label=u'Виберіть групу',
		help_text=u"Виберіть Групу",
		error_messages={'required': u"Поле Групи є обов’язковим",
						'invalid_choice': u'Неправильна група'}
		)

	study_start = forms.DateField(
		label=u"Початок навчання*",
		initial="2014-09-01",
		help_text=u"Початок навчання у форматі РРРР-ММ-ДД",
		error_messages={'required': u"Поле Початку Навчання є обов’язковим"}
		)

	student_journal = forms.ModelChoiceField(
		label=u'Журнал Відвідуванння',
		required=False,
		help_text=u'Виберіть журнал відвідування',
		queryset=Visiting.objects.all(),
		empty_label=u'Виберіть журнал відвідування'
		)

	no_field = forms.CharField(required=False)

class StudentEditView(UpdateView):
	"""docstring for StudentEditView"""
	
	model = Student
	template_name = 'students/students_edit3.html'
	pk_url_kwarg = 'sid'
	form_class = StudentEditForm

	def get_success_url(self):
		messages.success(self.request, u'Студента %s успішно збережено!' % self.object)
		return reverse('home')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(self.request, u'Редагування студента %s відмінено!' % self.get_object())
			return HttpResponseRedirect(reverse('home'))
		else:
			return super(StudentEditView, self).post(request, *args, **kwargs)

	def form_valid(self, form):
		"""Check if student is leader in any group.

		If yes? then ensure it's the same as selected group."""
		# get groups where is this student
		groups = Group.objects.filter(leader=self.object)
		if len(groups) > 0 and form.cleaned_data['student_group'] != groups[0]:
			messages.error(self.request, u'Студент є старостою іншої групи')
			return self.render_to_response(self.get_context_data(form=form))

		return super(StudentEditView, self).form_valid(form)

class StudentAddView(CreateView):
	model = Student
	template_name = 'students/students_edit3.html'
	form_class = StudentEditForm

	def get_success_url(self):
		messages.success(self.request, u'Студента %s успішно збережено!' % self.object)
		return reverse('home')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(self.request, u'Створення студента відмінено!')
			return HttpResponseRedirect(reverse('home'))
		else:
			return super(StudentAddView, self).post(request, *args, **kwargs)

class StudentDeleteView(DeleteView):
	"""docstring for StudentDeleteView"""
	model = Student
	template_name = 'students/students_confirm_delete.html'
	pk_url_kwarg = 'sid'

	def get_success_url(self):
		messages.success(self.request, u'Студента %s успішно видалено!' % self.object)
		return reverse('home')

class StudentDeleteView2(DetailView):
	template_name = 'students/students_confirm_delete.html'
	pk_url_kwarg = 'sid'
	model = Student

	def dispatch(self, request, *args, **kwargs):
		if request.method == "POST":
			if request.POST.get("delete_button"):
				messages.success(request, "%s was deleted success!" % self.get_object())
				self.get_object().delete()
				return HttpResponseRedirect(reverse('home'))
		return super(StudentDeleteView2, self).dispatch(request, *args, **kwargs)

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

def students_add2(request):
	if request.method == 'POST':
		form = StudentEditForm(request.POST, request.FILES)

		if request.POST.get('add_button') is not None:
			data = {}

			if form.is_valid():
				data['first_name'] = form.cleaned_data['first_name']
				data['last_name'] = form.cleaned_data['last_name']
				data['middle_name'] = form.cleaned_data['middle_name']
				data['birthday'] = form.cleaned_data['birthday']
				
				actWithPhoto = form.cleaned_data['actWithPhoto']
				if actWithPhoto == 'change':
					try:
						photo = form.cleaned_data['photo']
						if photo:
							sizePhoto = photo.size
							if sizePhoto > SIZE_LIMIT_FILE:
								raise tooBigPhotoError()
						else:
							raise NoPhotoError()
					
					except tooBigPhotoError:
						messages.error(request, (u"Невдале редагування %s! " % student) + u"Розмір фото не може перевищувати " + str(SIZE_LIMIT_FILE) + u" байт.\
											Додиний файл містить " + str(sizePhoto) + u" байт")
						return HttpResponseRedirect(reverse('home'))
					except NoPhotoError:
						messages.error(request, (u"Невдале редагування %s! " % student) + u'Виберіть фото. Ви натиснули кнопку змінити фото')
						return HttpResponseRedirect(reverse('home'))
					else:
						data['photo'] = form.cleaned_data['photo']
				elif actWithPhoto == 'drop':
					data['photo'] = None

				data['ticket'] = form.cleaned_data['ticket']
				data['notes'] = form.cleaned_data['notes']
				data['student_group'] = form.cleaned_data['student_group']
				data['study_start'] = form.cleaned_data['study_start']
				data['student_journal'] = form.cleaned_data['student_journal']
				try:
					student = Student(**data)
					student.save()
				except Exception as e:
					messages.error(request, (u"Невдале редагування %s!" % student) + str(e))
				else:
					messages.success(request, u"%s був поредагований успішно!" % student)

				return HttpResponseRedirect(reverse('home'))
			else:
				messages.info(request, "Validation errors")
				return render(request, 'students/students_add2.html',
					{'groups': Group.objects.all().order_by('title'),
					 'journals': Visiting.objects.all().order_by('title'),
					 'form': form})
		elif request.POST.get('cancel_button') is not None:
			messages.info(request, u"Додавання студента скасовано!")
			return HttpResponseRedirect(reverse('home'))
	else:
		form = StudentEditForm()
		return render(request, 'students/students_add2.html', {'form': form})

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

def students_edit2(request, sid):
	student = Student.objects.filter(pk=sid)[0]

	if request.method == 'POST':
		form = StudentEditForm(request.POST, request.FILES)

		if request.POST.get('edit_button') is not None:
			if form.is_valid():
				student.first_name = form.cleaned_data['first_name']
				student.last_name = form.cleaned_data['last_name']
				student.middle_name = form.cleaned_data['middle_name']
				student.birthday = form.cleaned_data['birthday']
				
				actWithPhoto = form.cleaned_data['actWithPhoto']
				if actWithPhoto == 'change':
					try:
						photo = form.cleaned_data['photo']
						if photo:
							sizePhoto = photo.size
							if sizePhoto > SIZE_LIMIT_FILE:
								raise tooBigPhotoError()
						else:
							raise NoPhotoError()
					
					except tooBigPhotoError:
						messages.error(request, (u"Невдале редагування %s! " % student) + u"Розмір фото не може перевищувати " + str(SIZE_LIMIT_FILE) + u" байт.\
											Додиний файл містить " + str(sizePhoto) + u" байт")
						return HttpResponseRedirect(reverse('home'))
					except NoPhotoError:
						messages.error(request, (u"Невдале редагування %s! " % student) + u'Виберіть фото. Ви натиснули кнопку змінити фото')
						return HttpResponseRedirect(reverse('home'))
					else:
						student.photo = form.cleaned_data['photo']
				elif actWithPhoto == 'drop':
					student.photo = None

				student.ticket = form.cleaned_data['ticket']
				student.notes = form.cleaned_data['notes']
				student.student_group = form.cleaned_data['student_group']
				student.study_start = form.cleaned_data['study_start']
				student.student_journal = form.cleaned_data['student_journal']
				try:
					student.save()
				except Exception as e:
					messages.error(request, (u"Невдале редагування %s!" % student) + str(e))
				else:
					messages.success(request, u"%s був поредагований успішно!" % student)

				return HttpResponseRedirect(reverse('home'))
			else:
				messages.info(request, "Validation errors")
				return render(request, 'students/students_edit2.html',
					{'groups': Group.objects.all().order_by('title'),
					 'journals': Visiting.objects.all().order_by('title'),
					 'sid': sid,
					 'form': form})
		#if cancel_button was pushed
		elif request.POST.get('cancel_button') is not None:
			messages.info(request, u"Редагування скасовано!")
			return HttpResponseRedirect(reverse('home'))	
	#is form wasn't posted
	else:
		default = {'first_name': student.first_name,
				   'last_name': student.last_name,
				   'middle_name': student.middle_name,
				   'birthday': student.birthday,
				   'photo': student.photo,
				   'actWithPhoto': 'leave',
				   'ticket': student.ticket,
				   'notes': student.notes,
				   'student_group': student.student_group,
				   'study_start': student.study_start,
				   'student_journal': student.student_journal}

		form = StudentEditForm(default)
		#give code of begin state
		return render(request, 'students/students_edit2.html',
			{'sid': sid,
			 'student': default,
			 'form': form})

def students_edit(request, sid):
	student = Student.objects.filter(pk=sid)[0]
	#if form was posted
	if request.method == 'POST':
		#if edit_button was pushed
		if request.POST.get('edit_button') is not None:
			#errors collections
			errors = {}
			# validate student data will go here
			data = {'middle_name': request.POST.get('middleName', '').strip(),
					'notes': request.POST.get('notes', '').strip()}
			
			student_journal = request.POST.get('journal', '').strip()
			if student_journal == '':
				data['student_journal'] = None
			else:
				journals = Visiting.objects.filter(pk=student_journal)
				if len(journals) != 1:
					errors['student_journal'] = "insert correct student journal"
				else:
					data['student_journal'] = journals[0]

			# validate user input
			first_name = request.POST.get('firstName', '').strip()
			if not first_name:
				errors['first_name'] = "First name is mandatory"
			else:
				data['first_name'] = first_name

			last_name = request.POST.get('lastName', '').strip()
			if not last_name:
				errors['last_name'] = "Last name is mandatory"
			else:
				data['last_name'] = last_name

			birthday = request.POST.get('birthday', '').strip()
			if not birthday:
				errors['birthday'] = "Date of birth is mandatory"
			else:
				try:
					datetime.strptime(birthday, '%Y-%m-%d')
				except Exception as e:
					errors['birthday'] = "Insert correct date format (e.g. 1974-11-5)" + str(e)
				else:
					data['birthday'] = birthday

			ticket = request.POST.get('ticket', '').strip()
			if not ticket:
				errors['ticket'] = "Ticket is mandatory"
			else:
				data['ticket'] = ticket

			study_start = request.POST.get('study_start', '').strip()
			if not study_start:
				errors['study_start'] = "Beginning of study is mandatory"
			else:
				try:
					datetime.strptime(study_start, "%Y-%m-%d")
				except Exception as e:
					errors['study_start'] = "Insert correct date format" + str(e)
				else:
					data['study_start'] = study_start

			student_group = request.POST.get('student_group', '').strip()
			if not student_group:
				errors['student_group'] = 'Change any student group'
			else:
				try:
					groups = Group.objects.filter(pk=student_group)
				except Exception as e:
					errors['student_group'] = str(e)
				else:
					pass
					if len(groups) != 1:
						errors['student_group'] = 'Insert correct group'
					else:
						data['student_group'] = groups[0]

			actWithPhoto = request.POST.get('pho', '')
			if actWithPhoto == 'change':
				data['photo'] = request.FILES.get('photo')
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
			elif actWithPhoto == 'delete':
				data['photo'] = None 

			if not errors:
				student.first_name = data['first_name']
				student.last_name = data['last_name']
				student.middle_name = data['middle_name']
				student.birthday = data['birthday']
				student.ticket = data['ticket']
				if 'photo' in data:
					student.photo = data['photo']
				student.notes = data['notes']
				student.study_start = data['study_start']
				student.student_group = data['student_group']
				student.student_journal = data['student_journal']
				
				student.save()
				messages.success(request, "%s was edited success!" % student)
				#returns user to list of students
				return HttpResponseRedirect(reverse('home'))
			else:
				messages.info(request, "Validation errors")
				return render(request, 'students/students_edit.html',
					{'groups': Group.objects.all().order_by('title'),
					 'journals': Visiting.objects.all().order_by('title'),
					 'errors': errors,
					 'sid': sid,
					 'student': student,
					 'actWithPhoto': "actWithPhoto"})
		#if cancel_button was pushed
		elif request.POST.get('cancel_button') is not None:
			messages.info(request, "Changes were canceled!")
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

def students_delete2(request, sid):
	student = Student.objects.filter(pk=sid)[0]

	if request.method == 'POST':
		if request.POST.get('delete_button') is not None:
			student.delete()
			messages.success(request, "%s was deleted success!" % student)
			return HttpResponseRedirect(reverse('home'))
	else:
		return render(request, 'students/students_confirm_delete2.html', {'sid': sid,
																		'student': student})

def students_delete_mult(request):
	students = Student.objects.all()

	if request.method == "POST":
		if request.POST.get('delete_button') is not None:
			delList = []
			for student in students:
				if request.POST.get(str(student.id)) is not None:
					delList.append(student)
			return render(request, 'students/students_confirm_delete_mult.html', {'students': delList})
		elif request.POST.get('delete_button_confirm') is not None:
			delMsg = ''
			for student in students:
				if request.POST.get(str(student.id)) is not None:
					delMsg += student.first_name + ' ' + student.last_name + ', '
					student.delete()
			if delMsg is not '':
				delMsg = delMsg[:-2] + ' '
				messages.success(request, delMsg + "were deleted success!")
			else:
				messages.info(request, "deletetion was canceled!")
			
			return HttpResponseRedirect(reverse('home'))

	return render(request, 'students/students_confirm_delete_mult.html', {'students': students})

