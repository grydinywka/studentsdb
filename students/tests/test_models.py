from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import Student, Group, MonthJournal, Exam, Result_exam
from ..models.Result_exam import validate_value

from datetime import datetime, date

class StudentModelTests(TestCase):
	"""Test student model"""

	def test_unicode(self):
		student = Student(first_name='Demo', last_name='Student')
		self.assertEqual(unicode(student), u'Demo Student')

class GroupModelTests(TestCase):
	"""Test student model"""

	def test_unicode(self):
		student, created = Student.objects.get_or_create(
			first_name="Illia",
			last_name="Petrov",
			birthday=date(2000, 12, 5),
			ticket=12345,
			study_start=date(2007, 9, 1))
		group = Group(title='The_best')
		group2 = Group(title='Good_group', leader=student)

		self.assertEqual(unicode(group), u'The_best')
		self.assertEqual(unicode(group2), u'Good_group (Illia Petrov)')

class MonthJournalModelTests(TestCase):
	"""test month_journal model"""

	def test_unicode(self):
		student, created = Student.objects.get_or_create(
			first_name="Illia",
			last_name="Petrov",
			birthday=date(2000, 12, 5),
			ticket=12345,
			study_start=date(2007, 9, 1))
		month_journal = MonthJournal.objects.get_or_create(student=student, date=date(2015, 10, 12))[0]
		self.assertEqual(unicode(month_journal), u'Student Petrov: Month:10, Year:2015')

class ExamModelTests(TestCase):
	"""test exam model"""

	def test_unicode(self):
		exam = Exam(title='Chemistry')
		self.assertEqual(exam.__unicode__(), u'Chemistry')

class ResultExamModelTests(TestCase):
	"""test result_exam model"""

	def test_unicode(self):
		exam = Exam(title='English',
					exam_date=datetime(2015, 10, 12, 10, 1, 0),
					presenter=u'Simonenko')
		student, created = Student.objects.get_or_create(
			first_name="Illia",
			last_name="Petrov",
			birthday=date(2000, 12, 5),
			ticket=12345,
			study_start=date(2007, 9, 1))
		result_exam = Result_exam(valuetion=9)
		result_exam.save()
		result_exam.students.add(student)
		self.assertEqual(result_exam.__unicode__(), u'9')
		self.assertRaises(ValidationError, validate_value, result_exam.valuetion+12)
		self.assertIn(student, result_exam.students.all()) # check if is out 'student' in list's result_exam
		
