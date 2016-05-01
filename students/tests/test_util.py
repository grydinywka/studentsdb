from django.test import TestCase
from django.http import HttpRequest

from students.models import Student, Group
from students.util import get_groups, get_current_group, paginate

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

