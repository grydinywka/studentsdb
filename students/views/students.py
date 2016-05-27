from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView
from django.utils.translation import ugettext as _

from ..models.Student import Student
from ..models.Group import Group
from ..models.Visiting import Visiting

from datetime import datetime
from PIL import Image

from ..util import paginate, boundsStuds, get_current_group

# import sys
# sys.path.append('/data/work/virtualenvs/studDb/src/studDb/studDb/')
from studDb.settings import SIZE_LIMIT_FILE

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import FormActions

class isNotImageError(Exception): pass
class tooBigPhotoError(Exception): pass
class NoPhotoError(Exception): pass

class StudentList(ListView):
	"""docstring for StudentList"""
	model = Student
	# queryset = Student.objects.all()
	template_name = 'students/students_list_for_cbv.html'
	context_object_name = 'students'
	# template = 'students/student_class_based_view_template'
	# paginate_by = 5

	def get_context_data(self, **kwargs):
		"""This method adds extra variables to template"""
		#get original context data from parent class
		context = super(StudentList, self).get_context_data(**kwargs)

		students = context['students']
		# try to order students list
		order_by = self.request.GET.get('order_by', '')
		if order_by in ('id', 'last_name', 'first_name', 'ticket'):
			students = students.order_by(order_by)
			if self.request.GET.get('reverse', '') == '1':
				students = students.reverse()

		paginate_by = 5
		context = paginate(students, paginate_by, self.request, context, var_name='students')

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

		# check if we need to show only one group of students
		current_group = get_current_group(self.request)
		if current_group:
			return qs.filter(student_group=current_group)
		else:
			# otherwise show all students
			return qs.order_by('last_name')

class StudentUpdateView(UpdateView):
	"""docstring for StudentUpdateView"""
	
	model = Student
	template_name = 'students/students_edit3.html'
	pk_url_kwarg = 'sid'

	def get_success_url(self):
		messages.success(self.request, _(u"Student was changed successfull!"))
		return reverse('home')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(self.request, _(u"Edition of student was canceled"))
			return HttpResponseRedirect(reverse('home'))
		else:
			return super(StudentUpdateView, self).post(request, *args, **kwargs)


# Class form for edit students
class StudentEditForm(forms.ModelForm):
	"""docstring for StudentEditForm"""
	class Meta:
		model = Student
		fields = '__all__'
		exclude = ()

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
		self.helper.form_class = 'form-horizontal a'

		# set form field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = False
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'
		
		# add buttons
		if 'instance' in kwargs:
			if kwargs['instance']:
				self.helper.layout[-1] = FormActions(
					Submit('edit_button', _(u'Edit'), css_class="btn btn-primary"),
					Submit('cancel_button', _(u'Cancel'), css_class="btn btn-link")
					)
			else:
				self.helper.layout[-1] = FormActions(
					Submit('add_button', _(u'Add'), css_class="btn btn-primary"),
					Submit('cancel_button', _(u'Cancel'), css_class="btn btn-link")
					)
		else:
			self.helper.layout[-1] = FormActions(
				Submit('add_button', _(u'Add'), css_class="btn btn-primary"),
				Submit('cancel_button', _(u'Cancel'), css_class="btn btn-link")
				)
		# self.helper.layout = Layout(
		# 	Field('first_name', css_id='ajax-edit-form'),
		# )

	def clean(self, value=None):
		if value is not None:
			groups = Group.objects.filter(leader=value)
			if len(groups) > 0 and self.cleaned_data.get('student_group') != groups[0]:
				raise forms.ValidationError('No name')
		return self.cleaned_data

	first_name = forms.CharField(
		label=_(u'Name*'),
		initial=_(u"Andrew"),
		max_length=100,
		help_text=_(u"Input your name"),
		error_messages={'required': _(u"Name is mandatory!")}
		)

	last_name = forms.CharField(
		label=_(u'Surname*'),
		initial=_(u"Koval"),
		help_text=_(u"Input your last name"),
		error_messages={'required': _(u"Surname is mandatory!")}
		)

	middle_name = forms.CharField(
		label=_(u'Middle name'),
		required=False
		)

	birthday = forms.DateField(
		label=_(u"Date of birth*"),
		initial="1970-2-24",
		help_text=_(u"Your date of birth in YYYY-MM-DD format"),
		error_messages={'required': _(u"Field date of birth is mandatory"),
						'invalid': _(u"Input valid format of date")}
		)

	# actWithPhoto = forms.ChoiceField(
	# 	label=_(u'Action with photo*:'),
	# 	widget=forms.RadioSelect,
	# 	choices=(('leave', 'Leave',), ('change', 'Edit',), ('drop', 'Delete',),)
	# 	)

	photo = forms.ImageField(
		label=_(u'Photo'),
		help_text=_(u'Choose Photo'),
		required=False,
		error_messages={'invalid': _(u'Your photo is not valid!'),
						'required': _(u'Photo is mandatory')}
		)

	ticket = forms.IntegerField(
		label=_(u'Ticket*'),
		help_text=_(u'Ticket #'),
		min_value=1,
		max_value=999999,
		error_messages={'min_value': _(u'At least 1!')}
		)

	notes = forms.CharField(
		label=_(u'Note'),
		help_text=_(u'Addition information'),
		max_length=2000,
		required=False
		)

	student_group = forms.ModelChoiceField(
		label=_(u'Group*'),
		queryset=Group.objects.all(),
		empty_label=_(u'Choose Group'),
		help_text=_(u"Choose Group"),
		error_messages={'required': _(u"Field Group is mandatory"),
						'invalid_choice': _(u'Invalid group')}
		)

	study_start = forms.DateField(
		label=_(u"Study begin*"),
		initial="2014-09-01",
		help_text=_(u"Start of study at YYYY-MM-DD format"),
		error_messages={'required': _(u"Field of Study begin is mandatory")}
		)

	student_journal = forms.ModelChoiceField(
		label=_(u'Visiting'),
		required=False,
		help_text=_(u'Choose journal'),
		queryset=Visiting.objects.all(),
		empty_label=_(u'Choose journal')
		)

	no_field = forms.CharField(required=False)

class StudentEditView(UpdateView):
	"""docstring for StudentEditView"""
	
	model = Student
	template_name = 'students/students_edit3.html'
	pk_url_kwarg = 'sid'
	form_class = StudentEditForm

	def get_success_url(self):
		messages.success(self.request, _(u'Student %s successfully saved!') % self.object)
		return reverse('home')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(self.request, _(u'Editing of student %s canceled!') % self.get_object())
			return HttpResponseRedirect(reverse('home'))
		else:
			return super(StudentEditView, self).post(request, *args, **kwargs)

	def form_valid(self, form):
		"""Check if student is leader in any group.

		If yes? then ensure it's the same as selected group."""
		# get groups where is this student
		groups = Group.objects.filter(leader=self.object)
		if len(groups) > 0 and form.cleaned_data['student_group'] != groups[0]:
			messages.error(self.request, _(u'Student {} is leader of other group').format(self.object))
			return self.render_to_response(self.get_context_data(form=form))

		return super(StudentEditView, self).form_valid(form)

	def form_invalid(self, form):
		"""
		If the form is invalid, re-render the context data with the
		data-filled form and errors.
		"""
		messages.info(self.request, _(u'Errors during editing %s student!' % self.object))
		return super(StudentEditView, self).form_invalid(form)

	def get_context_data(self, **kwargs):
		context = super(StudentEditView, self).get_context_data(**kwargs)
		context['title'] = _(u'Edit student')

		return context

class StudentAddView(CreateView):
	model = Student
	template_name = 'students/students_edit3.html'
	form_class = StudentEditForm

	def get_success_url(self):
		messages.success(self.request, _(u'Student %s successfull saved!') % self.object)
		return reverse('home')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(self.request, _(u'Creating student canceled!'))
			return HttpResponseRedirect(reverse('home'))
		else:
			return super(StudentAddView, self).post(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(StudentAddView, self).get_context_data(**kwargs)
		context['title'] = _(u'Add student')

		return context

	def form_invalid(self, form):
		"""
		If the form is invalid, re-render the context data with the
		data-filled form and errors.
		"""
		messages.info(self.request, _(u'Errors during creating student!'))
		return self.render_to_response(self.get_context_data(form=form))

class StudentDeleteView(DeleteView):
	"""docstring for StudentDeleteView"""
	model = Student
	template_name = 'students/students_confirm_delete.html'
	pk_url_kwarg = 'sid'

	def get_success_url(self):
		messages.success(self.request, _(u'Student %s successful deleted!' % self.object))
		return reverse('home')

class StudentDeleteView2(DetailView):
	template_name = 'students/students_confirm_delete.html'
	pk_url_kwarg = 'sid'
	model = Student

	def dispatch(self, request, *args, **kwargs):
		if request.method == "POST":
			if request.POST.get("delete_button"):
				messages.success(request, _(u"%s was deleted success!" % self.get_object()))
				self.get_object().delete()
			elif request.POST.get("cancel_button"):
				messages.success(request, _(u"Deletetion was canceled!"))
			
			return HttpResponseRedirect(reverse('home'))
		return super(StudentDeleteView2, self).dispatch(request, *args, **kwargs)

# Views for Students
def students_list(request):
	current_group = get_current_group(request)
	if current_group:
		students = Student.objects.filter(student_group=current_group)
	else:
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

	return render(request, 'students/students_list.html', {'students': students,
														   'valPage': valPage,
														   'listOfPage': listOfPage})

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
						messages.error(request, _((u"It is not good editing {}. \
												Size of photo do not allowed be more {} bite. \
												Added file contain {} bite").format(student,
																					  str(SIZE_LIMIT_FILE),
																					  str(sizePhoto)))
						)
						return HttpResponseRedirect(reverse('home'))
					except NoPhotoError:
						messages.error(request, _((u"It is not good editing {}! Choose a Photo. You pushed change button").format(student)))
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
					messages.error(request, (u"It is not good editing %s!" % student) + str(e))
				else:
					messages.success(request, u"%s was edited success!" % student)

				return HttpResponseRedirect(reverse('home'))
			else:
				messages.info(request, _(u"Validation errors"))
				return render(request, 'students/students_add2.html',
					{'groups': Group.objects.all().order_by('title'),
					 'journals': Visiting.objects.all().order_by('title'),
					 'form': form})
		elif request.POST.get('cancel_button') is not None:
			messages.info(request, _(u"Adding student was canceled!"))
			return HttpResponseRedirect(reverse('home'))
	else:
		form = StudentEditForm()
		return render(request, 'students/students_add2.html', {'form': form})

def students_add(request):
	# If form was posted
	if request.method == "POST":
		
		# If 'add button' was pressed
		if request.POST.get('add_button') is not None:
			
			# validate input from user
			errors = {}

			# validate student data
			data = {'middle_name': request.POST.get('middle_name'),
					'notes': request.POST.get('notes'),
					'student_journal': request.POST.get('student_journal')}

			#validate user input
			first_name = request.POST.get('first_name', '').strip()
			if not first_name:
				errors['first_name'] = _(u"Name is mandatory!")
			else:
				data['first_name'] = first_name

			last_name = request.POST.get('last_name', '').strip()
			if not last_name:
				errors['last_name'] = _(u"Surname is mandatory!")
			else:
				data['last_name'] = last_name
			
			birthday = request.POST.get('birthday', '').strip()
			if not birthday:
				errors['birthday'] = _(u"Date of birth is mandatory!")
			else:
				try:
					datetime.strptime(birthday, '%Y-%m-%d')
				except Exception:
					errors['birthday'] = _(u"Input date at YYYY-MM-DD format")
				else:
					data['birthday'] = birthday
			
			ticket = request.POST.get('ticket', '').strip()
			if not ticket:
				errors['ticket'] = _(u"Ticket is mandatory!")
			else:
				data['ticket'] = ticket
			
			student_group = request.POST.get('student_group', '').strip()
			if not student_group:
				errors['student_group'] = _(u"Choose a group for student!")
			else:
				groups = Group.objects.filter(pk=student_group)
				if len(groups) != 1:
					errors['student_group'] = _(u"Choose valid group!")
				else:
					data['student_group'] = groups[0]

			study_start = request.POST.get('study_start', '').strip()
			if not study_start:
				errors['study_start'] = _(u"Field study begin is mandatory!")
			else:
				try:
					datetime.strptime(study_start, '%Y-%m-%d')
				except Exception:
					errors['study_start'] = _(u"Input date at YYYY-MM-DD format")
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
				errors['photo'] = _(u"Error during opening a photo")
			except AttributeError:
				pass
			except isNotImageError:
				errors['photo'] = _(u"It is not a image")
			except tooBigPhotoError:
				errors['photo'] = _((u"It is not good editing {}. \
									Size of photo do not allowed be more {} bite. \
									Added file contain {} bite").format(student,
																		  str(SIZE_LIMIT_FILE),
																		  str(sizePhoto)))
			else:
				data['photo'] = photo
			
			if not errors:
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
				
				messages.success(request, _(u"Student %s successful added!" % student))
				# Return user to list of student
				return HttpResponseRedirect(reverse('home'))
			
			# If data were input incorrect:
			else:
				messages.warning(request, _(u"Please, correct next errors!"))
				# Return template together with errors
				return render(request, 'students/students_add.html',
					{'groups': Group.objects.all().order_by('title'),
					 'errors': errors})
		# if 'cancel button' was pressed:
		elif request.POST.get('cancel_button') is not None:
			messages.info(request, _(u"Adding student canceled!"))
			# Return user to list of student 
			return HttpResponseRedirect(reverse('home'))
	# If form was not posted:
	else:
		# return code begit state form
		return render(request, 'students/students_add.html',
			{'groups': Group.objects.all().order_by('title')})

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
					delMsg += _((u"{} {}, ").format(student.first_name, student.last_name))
					
					student.delete()
			if delMsg is not '':
				delMsg = delMsg[:-2] + ' '
				messages.success(request, delMsg + _(u"were deleted success!"))
			else:
				messages.info(request, _(u"deletetion was canceled!"))
			
			return HttpResponseRedirect(reverse('home'))

	return render(request, 'students/students_confirm_delete_mult.html', {'students': students})
