# -*- coding: utf-8 -*-

from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.urlresolvers import reverse

from ..models.Group import Group
from ..models.Student import Student

from django.views.generic import DeleteView, UpdateView, CreateView
from django.views.generic.base import TemplateView

from ..util import paginate, boundsStuds

# class form for add/edit group
class GroupAddEditForm(forms.ModelForm):
	class Meta:
		model = Group

	# def clean(self):
	# 	cleaned_data = super(GroupAddEditForm, self).clean()
	# 	title = cleaned_data.get("title")

	# 	if title:
	# 		groups = Group.objects.filter(title=title)
	# 		if len(groups) != 0:
	# 			self._errors["title"] = [u"Група з такою назвою вже існує!"]
				
	# 	return cleaned_data

	# def clean_title(self):
	# 	title = self.cleaned_data['title']

	# 	if Group.objects.filter(title=title).exists():
	# 		self._errors["title"] = [u"Група з такою назвою вже існує!2"]
				
	# 	return title

	def validTitle(self):
		groups = Group.objects.filter(title=self)
		if len(groups) != 0:
			raise forms.ValidationError(u"Група з такою назвою вже існує!3")
	
	title = forms.CharField(
		label=u"Назва Групи*",
		# initial=u"NewGroup",
		max_length=10,
		help_text=u"<- Введіть назву групи.",
		error_messages={'required': u"Назва Групи є обов’язковою!"},
		validators=[validTitle]
		)

	leader = forms.ModelChoiceField(
		label=u"Староста Групи",
		required=False,
		queryset=Student.objects.all().order_by('last_name'),
		empty_label=u"Оберіть старосту Групи!",
		to_field_name="pk"
		)

	notes = forms.CharField(
		label=u"Нотатки",
		help_text=u"Додаткова інформація",
		required=False,
		max_length=1000
		)

class GroupList(TemplateView):
	template_name = 'students/groups_list_for_cbv.html'

	def get_context_data(self, **kwargs):
		context = super(GroupList, self).get_context_data(**kwargs)

		groups = Group.objects.order_by('title')
		order_by = self.request.GET.get('order_by', '')
		if order_by in ('id', 'title', 'leader'):
			groups = groups.order_by(order_by)
			if self.request.GET.get('reverse', '') == '1':
					groups = groups.reverse()

		paginate_by = 5
		context = paginate(groups, paginate_by, self.request, context, var_name='groups')

		return context

# Views for Groups
def groups_list(request):
	groups = Group.objects.all()
	allGroups = len(groups)
	valGroupsOnPage = int(request.GET.get('valgroups', 3))
	valPage = allGroups/valGroupsOnPage
	
	if allGroups % valGroupsOnPage != 0:
		valPage += 1
	listOfPage = [str(i) for i in xrange(1, valPage+1, 1)]

	order_by = request.GET.get('order_by', '')
	if order_by in ('id', 'title', 'leader'):
		groups = groups.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
				groups = groups.reverse()
	elif order_by == '':
		groups = groups.order_by('title')

	# paginator groups
	# paginator = Paginator(groups, 3)
	# page = request.GET.get('page')
	# try:
	# 	groups = paginator.page(page)
	# except PageNotAnInteger:
	# 	# If page is not an integer, deliver first page.
	# 	groups = paginator.page(1)
	# except EmptyPage:
	# 	# If page is out of range (e. g. 9999), deliver
	# 	# last page of results.
	# 	groups = paginator.page(paginator.num_pages)

	# my paginator groups
	page = request.GET.get('page', '')
	
	try:
		page = int(float(page))
	except ValueError:
		page = 1
	if page > valPage or page < 1:
		page = valPage
	
	large = valGroupsOnPage*page
	little = large - valGroupsOnPage
	if allGroups > 1:
		groups = groups[little:large]

	return render(request, 'students/groups_list.html', {'groups': groups,
														 'valPage': valPage,
														 'listOfPage': listOfPage})

def groups_add_django_form(request):
	if request.method == "POST":
		form = GroupAddEditForm(request.POST)
		if request.POST.get('add_button') is not None:
			data = {}

			if form.is_valid():
				# check unique title of group
				# groups = Group.objects.filter(title=form.cleaned_data['title'])
				# if len(groups) != 0:
				data['title'] = form.cleaned_data['title']
				# else:

				data['leader'] = form.cleaned_data['leader']
				data['notes'] = form.cleaned_data['notes']

				try:
					group = Group(**data)
					group.save()
				except Exception as e:
					messages.error(request, (u"Невдале редагування/створення групи!") + str(e))
				else:
					messages.success(request, u"Група була поредагований/створена успішно!")

				return HttpResponseRedirect(reverse('groups'))
			else:
				messages.error(request, u"Помилки Валідації")
				return render(request, 'students/groups_add_django_form.html',
							  {'form': form})
		elif request.POST.get('cancel_button') is not None:
			messages.info(request, u"Створення групи відмінено!")
			return HttpResponseRedirect(reverse('groups'))
	else:
		form = GroupAddEditForm()
		return render(request, 'students/groups_add_django_form.html', {'form': form})

def groups_add_handle(request):
	# return HttpResponse('<h1>Groups Add Form</h1>')
	if request.method == 'POST':
		if request.POST.get('add_button') is not None:
			errors = {}

			data = {'notes': request.POST.get('notes')}

			title = request.POST.get('title', '').strip()
			if not title:
				errors['title'] = u'Назва групи є обов’язковою!'
			elif title in [group.title for group in Group.objects.filter(title=title)]:
				errors['title'] = u'Така назва групи вже існує!'
			else:
				data['title'] = title

			leader = request.POST.get('leader', '').strip()
			if leader:
				students = Student.objects.filter(id=leader)
				if len(students) != 1:
					errors['leader'] = u'Виберіть студента правильно!'
				elif hasattr(students[0], "group"):
					errors['leader'] = u'Студент %s є старостою іншої групи!' % students[0]
				else:
					data['leader'] = students[0]

			if not errors:
				group = Group(**data)
				try:
					group.save()
				except Exception as e:
					messages.success(request, u'Помилка' + str(e))
				else:
					messages.success(request, u'Групу %s успішно додано' % group)
				return HttpResponseRedirect(reverse('groups'))
			else:
				messages.error(request, u'Є помилки - виправте їх!')
				return render(request, 'students/groups_add_handle.html', {'errors': errors,
												'students': Student.objects.all().order_by('last_name')})

		elif request.POST.get('cancel_button') is not None:
			messages.info(request, u'Додавання групи скасовано')
			return HttpResponseRedirect(reverse('groups'))
	else:
		return render(request, 'students/groups_add_handle.html', {'students': Student.objects.all().order_by('last_name')})

def groups_edit_handle(request, gid):
	group = Group.objects.filter(pk=gid)[0]
	if request.method == 'POST':
		if request.POST.get('edit_button') is not None:
			errors = {}

			data = {'notes': request.POST.get('notes')}

			title = request.POST.get('title', '').strip()
			oldTitle = request.POST.get('oldTitle', 'Nothing').strip()
			if not title:
				errors['title'] = u'Назва групи є обов’язковою!'
			elif title != oldTitle and title in [group.title for group in Group.objects.filter(title=title)]:
				errors['title'] = u'Така назва групи вже існує!'
			else:
				data['title'] = title

			leader = request.POST.get('leader', "").strip()
			if leader:
				students = Student.objects.filter(pk=leader)

				if len(students) == 1:
					if students[0] != group.leader and hasattr(students[0], "group"):
						errors['leader'] = u'Виберіть студента правильно! \
						Студент %s є старостою %s групи!' % (students[0], students[0].group)
					else:
						data['leader'] = students[0]
				elif len(students) == 0:
					data['leader'] = None
				else:
					errors['leader'] = u'Виберіть студента правильно!'

			if not errors:
				group.title = data['title']
				if "leader" in data:
					group.leader = data['leader']
				else:
					group.leader = None
				group.notes = data['notes']
				try:
					group.save()
				except Exception as e:
					messages.error(request, u'Помилка' + str(e))
				else:
					messages.success(request, u'Групу %s успішно поредаговано' % group)
				return HttpResponseRedirect(reverse('groups'))
			else:
				messages.error(request, u'Є помилки - виправте їх!')
				return render(request, 'students/groups_edit_handle.html', {'errors': errors,
												'students': Student.objects.all().order_by('last_name'),
												'group': group,
												'gid': gid})

		elif request.POST.get('cancel_button') is not None:
			messages.info(request, u'Додавання групи скасовано')
			return HttpResponseRedirect(reverse('groups'))
	else:
		return render(request, 'students/groups_edit_handle.html', {'students': Student.objects.all().order_by('last_name'),
																   'gid': gid,
																   'group': group})

def groups_delete_handle(request, gid):
	group = Group.objects.filter(pk=gid)[0]

	if request.method == 'POST':
		if request.POST.get('cancel_button') is not None:
			messages.info(request, u'Видалення групи %s скасовано!' % group)
			return HttpResponseRedirect(reverse('groups'))
		elif request.POST.get('delete_button') is not None:
			messages.success(request, u'Групу %s видалено!' % group)
			group.delete()
			return HttpResponseRedirect(reverse('groups'))
	else:
		return render(request, 'students/groups_confirm_delete_handle.html', {'group': group,
																			  'gid': gid})

class GroupDeleteView(DeleteView):
	"""docstring for GroupDeleteView"""
	model = Group
	template_name = 'students/groups_confirm_delete.html'
	pk_url_kwarg = 'gid'
	
	def get_success_url(self):
		messages.success(self.request, u'Групу %s успішно видалено!' % self.object)
		return reverse('groups')

class GroupEditView(UpdateView):
	"""docstring for GroupEditView"""
	model = Group
	template_name = 'students/groups_add_django_form.html'
	pk_url_kwarg = 'gid'
	# form_class = GroupAddEditForm

	def get_success_url(self):
		messages.success(self.request, u'Групу %s успішно збережено!' % self.object)
		return reverse('groups')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(request, u'Редагування групи %s відмінено!' % self.get_object())
			return HttpResponseRedirect(reverse('groups'))
		else:
			return super(GroupEditView, self).post(request, *args, **kwargs)

	def form_valid(self, form):
		"""Check is any leader at the group
		If not, check is he belong to this group"""
		# get groups where is this student
		studentsOurGroup = Student.objects.filter(student_group=self.object)
		leaderOurGroup = form.cleaned_data['leader']
		if leaderOurGroup is not None:
			if not leaderOurGroup in studentsOurGroup:
				messages.error(self.request, u'Студент не належить до даної групи!')
				return self.render_to_response(self.get_context_data(form=form))
		
		title = form.cleaned_data['title']
		groups = Group.objects.filter(title=title)
		if len(groups) == 1 and groups[0] != self.object:
			messages.error(self.request, 'Name of group is busy')
			return self.render_to_response(self.get_context_data(form=form))
		
		return super(GroupEditView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(GroupEditView, self).get_context_data(**kwargs)

		context['defAct'] = 'edit'

		return context

class GroupAddView(CreateView):
	model = Group
	template_name = 'students/groups_add.html'
	success_url = '/groups/'
	form_class = GroupAddEditForm

	def get_success_url(self):
		messages.success(self.request, u'Групу %s успішно створено!' % self.object)
		return reverse('groups')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(request, u'Скасовано створення нової групи!')
			return HttpResponseRedirect(reverse('groups'))
		elif request.POST.get('add_button'):
			return super(GroupAddView, self).post(request, *args, **kwargs)
