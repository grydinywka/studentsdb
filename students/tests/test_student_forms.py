# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from students.models import Student, Group

def return_input(input):
	return input

class TestStudentUpdateForm(TestCase):
	
	fixtures = ['students_test_data.json']

	def setUp(self):
		#remember test browser
		self.client = Client()

		# remember url to edit form
		self.url = reverse('students_edit', kwargs={'sid': 2})

	def test_form(self):
		# login as admin to access student edit form
		self.client.login(username='admin', password="admin")

		# get form and check few fields there
		response = self.client.get(self.url)

		# check response status
		self.assertEqual(response.status_code, 200)

		# check page title, few field titles on edit form
		self.assertIn(u'Редагувати', response.content)
		self.assertIn(u'Білет', response.content)
		self.assertIn(u'Прізвище', response.content)
		self.assertIn('name="edit_button"', response.content)
		self.assertIn('name="cancel_button"', response.content)
		self.assertIn('action="%s"' % self.url, response.content)
		# self.assertIn('c.jpg', response.content)

	def test_success(self):
		# login as admin to access student edit form
		self.client.login(username='admin', password='admin')

		# post form with valid data
		group = Group.objects.filter(title='Group2')[0]
		with open('static/img/my.jpeg') as photo_file:
			response = self.client.post(
				self.url,
				{
					'first_name': 'Updated Name',
					'last_name': 'Updated Last Name',
					'ticket': '22233',
					'student_group': group.id,
					'birthday': '1990-11-11',
					'study_start': '2011-9-1',
					'photo': photo_file
				},
				follow=True)
		
		# check response status
		self.assertEqual(response.status_code, 200)

		# test updated student details
		student = Student.objects.get(pk=2)
		self.assertEqual(student.first_name, 'Updated Name')
		self.assertEqual(student.last_name, 'Updated Last Name')
		self.assertEqual(student.ticket, '22233')
		self.assertEqual(student.student_group, group)
		try:
			import re
			m = re.search( u'./my(?P<x>.*).jpeg', student.photo.name)
			x = m.group(1)
		except AttributeError:
			self.assertEqual(True, False)
		else:
			self.assertEqual(True, True)

		# self.assertRaisesRegexp(AttributeError, u'./my(?P<x>.*).jpeg', return_input, student.photo.name)
		self.assertRegexpMatches(student.photo.name, u'./my(?P<x>.*).jpeg')

		# check proper redirect after form post
		self.assertIn(u'Студента %s успішно збережено!' % student, response.content)
		