# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from datetime import datetime, date

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from students.models import Student, Group

class TestStudentList(TestCase):

	def setUp(self):
		# create groups
		group1, created = Group.objects.get_or_create(
			title="MtM-1")
		group2, created = Group.objects.get_or_create(
			title="MtM-2")

		# create 4 students: 1 for group1 and 3 for group2
		Student.objects.get_or_create(
			first_name="Ivan",
			last_name="Ivanenko",
			birthday=date(2000, 12, 5),
			ticket=12345,
			student_group=group1,
			study_start=date(2007, 9, 1))
		Student.objects.get_or_create(
			first_name="Dmitro",
			last_name="Renko",
			birthday=date(2001, 12, 5),
			ticket=23456,
			student_group=group2,
			study_start=date(2007, 9, 1))
		Student.objects.get_or_create(
			first_name="Sashko",
			last_name="Solovko",
			birthday=date(2000, 12, 5),
			ticket=12045,
			student_group=group2,
			study_start=date(2007, 9, 1))
		Student.objects.get_or_create(
			first_name="Arkadiy",
			last_name="Chub",
			birthday=date(2000, 12, 5),
			ticket=1225,
			student_group=group2,
			study_start=date(2007, 9, 1))
		Student.objects.get_or_create(
			first_name="Roman",
			last_name="Zelov",
			birthday=date(2000, 12, 5),
			ticket=1225,
			student_group=group2,
			study_start=date(2007, 9, 1))
		Student.objects.get_or_create(
			first_name="Stas",
			last_name="Drozd",
			birthday=date(2000, 12, 5),
			ticket=1225,
			student_group=group2,
			study_start=date(2007, 9, 1))

		# remember test browser
		self.client = Client()

		# remember url to our homepage
		self.url = reverse('home')

	def test_students_list(self):
		# make request to the server to get homepage page
		response = self.client.get(self.url)

		# have we received OK status from the server?
		self.assertEqual(response.status_code, 200)

		# do we have student name on page?
		self.assertIn('Ivan', response.content)

		# do we have link to student edit form?
		self.assertIn(reverse('students_edit', kwargs={'sid': Student.objects.all()[0].id}),
					  response.content)
		# self.assertIn('/students/1/edit/',
		# 			  response.content)
		
		# ensure we got 5 students, pagination limit is 5
		self.assertEqual(len(response.context['students']), 5) 

	def test_current_group(self):
		# set group1 as currently selected group
		group = Group.objects.filter(title="MtM-1")[0]
		self.client.cookies['current_group'] = group.id

		# make request to the server to get homepage page
		response = self.client.get(self.url)

		# in group1 we have only 1 student
		self.assertEqual(len(response.context['students']), 1)

	def test_order_by(self):
		# set order by Last Name
		response = self.client.get(self.url, {'order_by': 'first_name'})

		# now check if we got proper order
		students = response.context['students']
		self.assertEqual(students[0].first_name, 'Arkadiy')
		self.assertEqual(students[1].first_name, 'Dmitro')
		self.assertEqual(students[2].first_name, 'Ivan')
		self.assertEqual(students[3].first_name, 'Roman')
		self.assertEqual(students[4].first_name, 'Sashko')

		response = self.client.get(self.url, {'order_by': 'first_name', 'page': '2'})
		students = response.context['students']
		self.assertEqual(students[0].first_name, 'Stas')

	def test_order_by_reverse(self):
		# set order by Last Name
		response = self.client.get(self.url, {'order_by': 'last_name', 'reverse': '1'})

		# now check if we got proper order
		students = response.context['students']
		self.assertEqual(students[0].last_name, 'Zelov')
		self.assertEqual(students[1].last_name, 'Solovko')
		self.assertEqual(students[2].last_name, 'Renko')
		self.assertEqual(students[3].last_name, 'Ivanenko')
		self.assertEqual(students[4].last_name, 'Drozd')

	def test_pagination(self):
		response = self.client.get(self.url, {'page': '1'})

		students = response.context['students']
		self.assertEqual(students[0].last_name, 'Chub')
		self.assertEqual(students[1].last_name, 'Drozd')
		self.assertEqual(students[2].last_name, 'Ivanenko')
		self.assertEqual(students[3].last_name, 'Renko')
		self.assertEqual(students[4].last_name, 'Solovko')

		response = self.client.get(self.url, {'page': '2'})

		students = response.context['students']
		self.assertEqual(students[0].last_name, 'Zelov')
