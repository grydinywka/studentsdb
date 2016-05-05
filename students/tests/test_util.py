from django.test import TestCase
from django.http import HttpRequest

from students.models import Student, Group
from students.util import get_groups, get_current_group, paginate, boundsStuds

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import date

class UtilsTestCase(TestCase):
	"""Test functions from util module"""
	
	def setUp(self):
		# create group
		group1, created = Group.objects.get_or_create(
			id=1,
			title="Group1")
		group2, created = Group.objects.get_or_create(
			id=2,
			title="Group2")
		group3, created = Group.objects.get_or_create(
			id=3,
			title="Group3")
		student1, created = Student.objects.get_or_create(
			id=1,
			first_name="Ivan",
			last_name="Ivanenko",
			birthday=date(2000, 12, 5),
			ticket=123,
			student_group=group1,
			study_start=date(2007, 9, 1))
		student2, created = Student.objects.get_or_create(
			id=2,
			first_name="Ivan2",
			last_name="Ivanenko2",
			birthday=date(2000, 12, 5),
			ticket=123,
			student_group=group1,
			study_start=date(2007, 9, 1))
		student3, created = Student.objects.get_or_create(
			id=3,
			first_name="Ivan3",
			last_name="Ivanenko3",
			birthday=date(2000, 12, 5),
			ticket=123,
			student_group=group2,
			study_start=date(2007, 9, 1))
		student4, created = Student.objects.get_or_create(
			id=4,
			first_name="Ivan4",
			last_name="Ivanenko4",
			birthday=date(2000, 12, 5),
			ticket=123,
			student_group=group2,
			study_start=date(2007, 9, 1))
		student5, created = Student.objects.get_or_create(
			id=5,
			first_name="Ivan5",
			last_name="Ivanenko5",
			birthday=date(2000, 12, 5),
			ticket=123,
			student_group=group3,
			study_start=date(2007, 9, 1))
		student6, created = Student.objects.get_or_create(
			id=6,
			first_name="Ivan6",
			last_name="Ivanenko6",
			birthday=date(2000, 12, 5),
			ticket=123,
			student_group=group3,
			study_start=date(2007, 9, 1))
		student7, created = Student.objects.get_or_create(
			id=7,
			first_name="Ivan7",
			last_name="Ivanenko7",
			birthday=date(2000, 12, 5),
			ticket=123,
			student_group=group3,
			study_start=date(2007, 9, 1))
		student8, created = Student.objects.get_or_create(
			id=8,
			first_name="Ivan8",
			last_name="Ivanenko8",
			birthday=date(2000, 12, 5),
			ticket=123,
			student_group=group3,
			study_start=date(2007, 9, 1))

	def test_get_current_group(self):
		# prepare request object to pass to utility function
		request = HttpRequest()

		# test with no group set in cookie
		request.COOKIES['current_group'] = ''
		self.assertEqual(None, get_current_group(request))

		# test with invalid group id
		request.COOKIES['current_group'] = '12345'
		self.assertEqual(None, get_current_group(request))

		# test with proper group identificator
		group = Group.objects.filter(title='Group1')[0]
		request.COOKIES['current_group'] = str(group.id)
		self.assertEqual(group, get_current_group(request))

	def test_get_group(self):
		request = HttpRequest()
		queryset_groups = Group.objects.all()

		request.COOKIES['current_group'] = queryset_groups.filter(title='Group1')[0]
		groups = get_groups(request)
		self.assertEqual(type([]), type(groups))

		value_groups = len(queryset_groups)
		self.assertEqual(value_groups, len(groups))

		
		for group in groups:
			self.assertTrue(len(queryset_groups.filter(pk=group['id'])))

	def test_paginate(self):
		request = HttpRequest()
		paginator = Paginator

		request.GET['page'] = 2
		size = 1
		objects = Group.objects.all()
		dict_context = {}

		paginator = paginator(objects, size)
		page = paginator.page(2)

		context = paginate(objects, size, request, dict_context)
		# self.assertTrue(page == context['object_list'])
		self.assertTrue(context['is_paginated'])
		# self.assertEqual(page, context['page_obj'])
		# self.assertEqual(paginator, context['paginator'])
		self.assertEqual(paginator.object_list, context['paginator'].object_list)

		self.assertRaises(EmptyPage, paginator.page, 1212)
		self.assertRaises(PageNotAnInteger, paginator.page, "number")

	def test_boundsStuds(self):
		students = Student.objects.all()
		request = HttpRequest()
		
		students_on_page = 3
		request.GET['page'] = '1'
		self.assertEqual((0,3), boundsStuds(students, students_on_page, request))

		request.GET['page'] = '2'
		self.assertEqual((3,6), boundsStuds(students, students_on_page, request))

		request.GET['page'] = '3'
		self.assertEqual((6,8), boundsStuds(students, students_on_page, request))

		students_on_page = 2
		request.GET['page'] = '1'
		self.assertEqual((0,2), boundsStuds(students, students_on_page, request))

		request.GET['page'] = '2'
		self.assertEqual((2,4), boundsStuds(students, students_on_page, request))

		request.GET['page'] = '3'
		self.assertEqual((4,6), boundsStuds(students, students_on_page, request))

		request.GET['page'] = '4'
		self.assertEqual((6,8), boundsStuds(students, students_on_page, request))

		request.GET['page'] = '56'
		self.assertEqual((6,8), boundsStuds(students, students_on_page, request))

		request.GET['page'] = '-23'
		self.assertEqual((0,2), boundsStuds(students, students_on_page, request))

		request.GET['page'] = 'strPage'
		self.assertEqual((0,2), boundsStuds(students, students_on_page, request))
		self.assertRaises(TypeError, boundsStuds(students, students_on_page, request))