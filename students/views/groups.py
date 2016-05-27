from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.generic import DeleteView, UpdateView, CreateView
from django.views.generic.base import TemplateView
from django.utils.translation import ugettext as _

from ..models.Group import Group
from ..models.Student import Student

from ..util import paginate, boundsStuds, get_current_group

# class form for add/edit group
class GroupAddEditForm(forms.ModelForm):
	class Meta:
		model = Group
		fields = '__all__'
		exclude = ()

	# def clean(self):
	# 	cleaned_data = super(GroupAddEditForm, self).clean()
	# 	title = cleaned_data.get("title")

	# 	if title:
	# 		groups = Group.objects.filter(title=title)
	# 		if len(groups) != 0:
	# 			self._errors["title"] = [_(u"Other group has the same title!")]
				
	# 	return cleaned_data

	# def clean_title(self):
	# 	title = self.cleaned_data['title']

	# 	if Group.objects.filter(title=title).exists():
	# 		self._errors["title"] = [_(u"Other group has the same title!2")]
				
	# 	return title

	def validTitle(self):
		groups = Group.objects.filter(title=self)
		if len(groups) != 0:
			raise forms.ValidationError(_(u"Other group has the same title!3"))
	
	title = forms.CharField(
		label=_(u"Title*"),
		# initial=u"NewGroup",
		max_length=10,
		help_text=_(u"<- Input title"),
		error_messages={'required': _(u"Title is mandatory!")},
		validators=[validTitle]
		)

	leader = forms.ModelChoiceField(
		label=_(u"Leader"),
		required=False,
		queryset=Student.objects.all().order_by('last_name'),
		empty_label=_(u"Choose leader"),
		to_field_name="pk"
		)

	notes = forms.CharField(
		label=_(u"Notes"),
		help_text=_(u"Additional info"),
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

		current_group = get_current_group(self.request)
		if current_group:
			groups = [current_group]
		# else:
		# 	groups = groups.filter(pk=current_group.pk)

		paginate_by = 5
		context = paginate(groups, paginate_by, self.request, context, var_name='groups')

		return context

	def get_queryset(self):
		qs = super(GroupList, self).get_queryset()

		# current_group = get_current_group(self.request)
		# if current_group:
		# 	return [current_group]
		# else:
		# 	return qs.filter(pk=8)
		return qs[:2]

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
					messages.error(request, _(u"Unsuccessful editing / creating group!") + str(e))
				else:
					messages.success(request, _(u"Group was edited / created successful!"))

				return HttpResponseRedirect(reverse('groups'))
			else:
				messages.error(request, _(u"Validation eroors"))
				return render(request, 'students/groups_add_django_form.html',
							  {'form': form})
		elif request.POST.get('cancel_button') is not None:
			messages.info(request, _(u"Creating group canceled!"))
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
				errors['title'] = _(u'Title is required!')
			elif title in [group.title for group in Group.objects.filter(title=title)]:
				errors['title'] = _(u'Other group group has the same title!')
			else:
				data['title'] = title

			leader = request.POST.get('leader', '').strip()
			if leader:
				students = Student.objects.filter(id=leader)
				if len(students) != 1:
					errors['leader'] = _(u'Choose student properly!')
				elif hasattr(students[0], "group"):
					errors['leader'] = _(u'Student %s is leader of another group!') % students[0]
				else:
					data['leader'] = students[0]

			if not errors:
				group = Group(**data)
				try:
					group.save()
				except Exception as e:
					messages.success(request, _(u'Error') + str(e))
				else:
					messages.success(request, _(u'Group %s successfully added') % group)
				return HttpResponseRedirect(reverse('groups'))
			else:
				messages.error(request, _(u'There are errors - fix them!'))
				return render(request, 'students/groups_add_handle.html', {'errors': errors,
												'students': Student.objects.all().order_by('last_name')})

		elif request.POST.get('cancel_button') is not None:
			messages.info(request, _(u'Adding group canceled!'))
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
				errors['title'] = _(u'Title is required!')
			elif title != oldTitle and title in [group.title for group in Group.objects.filter(title=title)]:
				errors['title'] = u'Other group has the same title!'
			else:
				data['title'] = title

			leader = request.POST.get('leader', "").strip()
			if leader:
				students = Student.objects.filter(pk=leader)

				if len(students) == 1:
					if students[0] != group.leader and hasattr(students[0], "group"):
						errors['leader'] = _(u'Choose student properly! Student {} is leader of {} group!').format(students[0], students[0].group)
					else:
						data['leader'] = students[0]
				elif len(students) == 0:
					data['leader'] = None
				else:
					errors['leader'] = _(u'Choose student properly!')

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
					messages.error(request, _(u'Error') + str(e))
				else:
					messages.success(request, _(u'Group %s successfully edited') % group)
				return HttpResponseRedirect(reverse('groups'))
			else:
				messages.error(request, _(u'Here are errors - fix them!'))
				return render(request, 'students/groups_edit_handle.html', {'errors': errors,
												'students': Student.objects.all().order_by('last_name'),
												'group': group,
												'gid': gid})

		elif request.POST.get('cancel_button') is not None:
			messages.info(request, _(u'Editing of group was canceled!'))
			return HttpResponseRedirect(reverse('groups'))
	else:
		return render(request, 'students/groups_edit_handle.html', {'students': Student.objects.all().order_by('last_name'),
																   'gid': gid,
																   'group': group})

def groups_delete_handle(request, gid):
	group = Group.objects.filter(pk=gid)[0]

	if request.method == 'POST':
		if request.POST.get('cancel_button') is not None:
			messages.info(request, _(u'Deletingg of group %s canceled!') % group)
			return HttpResponseRedirect(reverse('groups'))
		elif request.POST.get('delete_button') is not None:
			messages.success(request, _(u'Group %s deleted!') % group)
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
		messages.success(self.request, _(u'Group %s successfully deleted!') % self.object)
		return reverse('groups')

class GroupEditView(UpdateView):
	"""docstring for GroupEditView"""
	model = Group
	template_name = 'students/groups_add_django_form.html'
	pk_url_kwarg = 'gid'
	# form_class = GroupAddEditForm

	def get_success_url(self):
		messages.success(self.request, _(u'Group %s successfully saved!') % self.object)
		return reverse('groups')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(request, _(u'Editing group %s canceled!') % self.get_object())
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
				messages.error(self.request, _(u'Student belong to other group!'))
				return self.render_to_response(self.get_context_data(form=form))
		
		title = form.cleaned_data['title']
		groups = Group.objects.filter(title=title)
		if len(groups) == 1 and groups[0] != self.object:
			messages.error(self.request, _('Name of group is busy'))
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
		messages.success(self.request, _(u'Group %s successfully created!') % self.object)
		return reverse('groups')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(request, _(u'Creating new group was canceled!'))
			return HttpResponseRedirect(reverse('groups'))
		elif request.POST.get('add_button'):
			return super(GroupAddView, self).post(request, *args, **kwargs)
