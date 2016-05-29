from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr

from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView

from ..models import MonthJournal, Student, Group
from ..util import paginate, boundsStuds, get_current_group, get_custom_language

from copy import copy

class JournalView(TemplateView):
	template_name = 'students/journal.html'

	def post(self, request, *args, **kwargs):
		data = request.POST

		# prepare student, dates and presence data
		current_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
		month = date(current_date.year, current_date.month, 1)
		present = data['present'] and True or False
		student = Student.objects.get(pk=data['pk'])
		# group = Group.objects.get(pk=data['group_pk'])

		# get or create journal object for given student and month
		journal = MonthJournal.objects.get_or_create(student=student, date=month)[0]

		# set new presence on journal for given student and save result
		setattr(journal, 'present_day%d' % current_date.day, present)
		journal.save()

		# return success status
		return JsonResponse({'key': 'success'})

	def get_context_data111(self, **kwargs):
		# get context data from TemplateView class
		context = super(JournalView, self).get_context_data(**kwargs)

		# check if we need to display some specific month
		if self.request.GET.get('month'):
			month = datetime.strptime(self.request.GET['month'], '%Y-%m-%d'
				).date()
		else:
			# otherwise just displaying current month data
			today = datetime.today()
			month = date(today.year, today.month, 1)

		# calculate current previous and next month details;
		# We need this for month navigation element in template
		next_month = month + relativedelta(months=1)
		prev_month = month - relativedelta(months=1)
		context['prev_month'] = prev_month.strftime('%Y-%m-%d')
		context['next_month'] = next_month.strftime('%Y-%m-%d')
		context['year'] = month.year
		context['month_verbose'] = month.strftime('%B')

		# we'll use this variable in students pagination
		context['cur_month'] = month.strftime('%Y-%m-%d')

		# prepare variable for template to generate
		# journal table header elements
		myear, mmonth = month.year, month.month
		number_of_days = monthrange(myear, mmonth)[1]
		context['month_header'] = [{'day': d,
			'verbose': day_abbr[weekday(myear, mmonth, d)][:3]}
			for d in range(1, number_of_days+1)]

		page = self.request.GET.get('page', 1)
		valStudOnPage = 10
		queryset = Student.objects.order_by('last_name')
		allStudents = len(queryset)
		valPage = allStudents/valStudOnPage
		try:
			page = int(float(page))
		except ValueError:
			page = 1
		if page > valPage or page < 1:
			page = valPage

		large = valStudOnPage*page
		little = large - valStudOnPage
		# get students from database, value of ones depend from number of page
		# if allStudents > valStudOnPage:
		# q_pre = queryset[:little]
		# queryset = queryset[little:large]
		# q_after = queryset[large:]

		# url to update student presence, for form post
		update_url = reverse('journal')

		# go over all students and collect data about presence
		# during selected month
		students = []
		for student in queryset:
			# try to get journal object by month selected
			# month and current student
			try:
				journal = MonthJournal.objects.get(student=student, date=month)
			except Exception:
				journal = None

			# fill in days presence list for current student
			days = []
			for day in range(1, number_of_days+1):
				days.append({
					'day': day,
					'present': journal and getattr(journal, 'present_day%d' % day, False) or False,
					'date': date(myear, mmonth, day).strftime('%Y-%m-%d'),
				})

			# prepare metadata for current student
			students.append({
				'fullname': u'%s %s' % (student.last_name, student.first_name),
				'days': days,
				'id': student.id,
				'update_url': update_url,
			})

		# apply pagination, 10 students per page
		context = paginate(students, valStudOnPage, self.request, context,
			var_name='students')

		# finally return updated context
		# with paginated students
		return context

	def get_context_data(self, **kwargs):
		# import pdb;pdb.set_trace()
		# get context data from TemplateView class
		context = super(JournalView, self).get_context_data(**kwargs)

		# check if we need to display some specific month
		if self.request.GET.get('month'):
			month = datetime.strptime(self.request.GET['month'], '%Y-%m-%d'
				).date()
		else:
			# otherwise just displaying current month data
			today = datetime.today()
			month = date(today.year, today.month, 1)

		# calculate current previous and next month details;
		# We need this for month navigation element in template
		next_month = month + relativedelta(months=1)
		prev_month = month - relativedelta(months=1)
		context['prev_month'] = prev_month.strftime('%Y-%m-%d')
		context['next_month'] = next_month.strftime('%Y-%m-%d')
		context['year'] = month.year
		context['month_verbose'] = month.strftime('%B')
		context['exact_group'] = False # For /journal/group/#/

		# we'll use this variable in students pagination
		context['cur_month'] = month.strftime('%Y-%m-%d')

		# prepare variable for template to generate
		# journal table header elements
		myear, mmonth = month.year, month.month
		number_of_days = monthrange(myear, mmonth)[1]
		context['month_header'] = [{'day': d,
			'verbose': day_abbr[weekday(myear, mmonth, d)][:3]}
			for d in range(1, number_of_days+1)]

		valStudOnPage = 10

		# get all students from database, or just one if we need to display journal for one student
		if kwargs.get('pk'):
			queryset = [Student.objects.get(pk=kwargs['pk'])]
		elif kwargs.get('group_pk'):
			context['exact_group'] = Group.objects.get(pk=kwargs['group_pk'])
			queryset = Student.objects.filter(student_group=kwargs['group_pk'])
		else:
			current_group = get_current_group(self.request)
			if current_group:
				queryset = Student.objects.filter(student_group=current_group)
			else:
				queryset = Student.objects.order_by('last_name')
		students = [i for i in queryset]

		#define bounds of students' list
		little, large = boundsStuds(students, valStudOnPage, self.request)
		# context['little'] = little
		# context['large'] = large

		# url to update student presence, for form post
		update_url = reverse('journal')

		# go over all students and collect data about presence
		# during selected month
		i = little
		if len(queryset) > 0:
			while i < large:
				# try to get journal object by month selected
				# month and current student
				try:
					journal = MonthJournal.objects.get(student=queryset[i], date=month)
				except Exception:
					journal = None

				# fill in days presence list for current student
				days = []
				for day in range(1, number_of_days+1):
					days.append({
						'day': day,
						'present': journal and getattr(journal, 'present_day%d' % day, False) or False,
						'date': date(myear, mmonth, day).strftime('%Y-%m-%d'),
					})

				# prepare metadata for current student

				students[i] = {
					'fullname': u'%s %s' % (queryset[i].last_name, queryset[i].first_name),
					'days': days,
					'id': queryset[i].id,
					'update_url': update_url,
				}
				i += 1
				
		# apply pagination, 10 students per page
		context = paginate(students, valStudOnPage, self.request, context,
			var_name='students')
		
		# finally return updated context
		# with paginated students
		return context
