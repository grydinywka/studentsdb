import logging

from django.utils.six import StringIO
from django.test import TestCase

from students.models import Student, Group, MonthJournal, Exam, Result_exam
from students import signals

from datetime import date

# logger = logging.getLogger('students.signals')
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(levelname)s %(asctime)s %(module)s: %(message)s')
# ch.setFormatter(formatter)
# logger.addHandler(ch)

class StudentSignalTests(TestCase):
	"""Testing log_student_event"""

	def setUp(self):
		self.out = StringIO()
		self.handler = logging.StreamHandler(self.out)
		logging.root.addHandler(self.handler)

	def tearDown(self):
		logging.root.removeHandler(self.handler)

	def test_add_update_student_event(self):
		"""Check logging signal for newly created student"""
		# now create student, this should raise new message inside
		# our logger output file
		student, created = Student.objects.get_or_create(first_name="Illia",
			last_name="Petrov",
			birthday=date(2000, 12, 5),
			ticket=12345,
			study_start=date(2007, 9, 1))

		# check output file content
		self.out.seek(0)
		self.assertEqual(self.out.readlines()[-1],
			'Student added: Illia Petrov (ID: %d)\n' % student.id)

		# now update existing student and check last line in out
		student.ticket = '12345'
		student.save()
		self.out.seek(0)
		self.assertEqual(self.out.readlines()[-1],
			'Student updated: Illia Petrov (ID: %d)\n' % student.id)

	def test_log_student_delete_event(self):
		"""Test log deletetion student"""
		student, created = Student.objects.get_or_create(first_name="Illia",
			last_name="Petrov",
			birthday=date(2000, 12, 5),
			ticket=12345,
			study_start=date(2007, 9, 1))

		stud_id = student.id
		student.delete()

		self.out.seek(0)
		self.assertEqual(self.out.readlines()[-1], "Student deleted: Illia Petrov (ID: %d)\n" % stud_id)

	def test_log_group_add_update_event(self):
		student = Student(first_name='Demo', last_name='Student')
		student.save()
		group = Group(title='TTE')
		group.save()

		self.out.seek(0)

		self.assertEqual(self.out.readlines()[-1], "Group added: %s (ID: %d)\n" % (group.title, group.id))

		group.leader = student
		group.save()

		self.out.seek(0)

		self.assertEqual(self.out.readlines()[-1].strip(), "Group edited: {} (ID: {})".format(group.title, group.id))

	def test_log_group_delete(self):
		group = Group(title='The Best Title')
		group.save()

		group_id = group.id
		group_title = group.title
		group.delete()

		self.out.seek(0)

		self.assertEqual(self.out.readlines()[-1].strip(), "Group deleted: {0} (ID: {1})".format(group_title, group_id))

	def test_log_monthjournal_add_update(self):
		student = Student(first_name='Nick', last_name='Rest')
		student.save()
		monthjournal = MonthJournal(student=student, date=date(2016, 5, 2))
		monthjournal.save()

		self.out.seek(0)

		self.assertEqual(self.out.readlines()[-1].strip(), "MonthJournal created: %s" % monthjournal)

		monthjournal.present_day1 = True
		monthjournal.save()

		self.out.seek(0)

		self.assertEqual(self.out.readlines()[-1].strip(), "MonthJournal updated: %s" % monthjournal)

	def test_log_monthjournal_delete(self):
		student = Student(first_name='Kick', last_name='Resl')
		student.save()
		monthjournal = MonthJournal(student=student, date=date(2016, 5, 2))
		monthjournal.save()

		# import copy
		# mj = copy.deepcopy(monthjournal)
		mj = monthjournal

		monthjournal.delete()

		self.out.seek(0)

		self.assertEqual(self.out.readlines()[-1].strip(), "MonthJournal deleted: %s" % mj)

	def test_log_exam_add_update(self):
		group = Group(title='G-TTY')
		group.save()
		exam = Exam(title='Solphegio', exam_date=date(2016,5,12), presenter='Fedir Ivanovich')
		exam.save()
		

		self.out.seek(0)

		self.assertEqual(self.out.readlines()[-1].strip(), "Exam created: %s (ID: %d)" % (exam.title, exam.id))
		
		exam.exam_group.add(group)
		exam.save()

		self.assertEqual(exam.exam_group ,Exam.objects.filter(title='Solphegio')[0].exam_group)

		group2 = Group(title='Phisics')
		group2.save()
		exam.exam_group.add(group2)
		exam.save()

		self.out.seek(0)
		self.assertEqual(self.out.readlines()[-1].strip(), "Exam updated: %s (ID: %d)" % (exam.title, exam.id))

	def test_log_exam_delete(self):
		exam = Exam(title='Spanish', exam_date=date(2013,1,1), presenter='Petro P.')
		exam.save()

		copyexam = exam
		exam.delete()

		self.out.seek(0)

		self.assertEqual(self.out.readlines()[-1].strip(), "Exam deleted: %s" % copyexam)

	def test_log_exam_change_groups(self):
		group = Group(title='ASD')
		group.save()
		exam = Exam(title='Spanish', exam_date=date(2013,1,1), presenter='Petro P.')
		exam.save()
		exam.exam_group.add(group)
		exam.save()

		self.out.seek(0)

		info_str = "exam {} have next groups after modified:\n".format(exam)
		for exam_group in Exam.objects.filter(title='Spanish')[0].exam_group.all():
			info_str += exam_group.title + '\n'
		out_str = ''.join(self.out.readlines()[-4:-2])
		self.assertEqual(out_str, info_str)

	def test_log_result_exam_add_update(self):
		result_exam = Result_exam(valuetion=2)
		result_exam.save()

		self.out.seek(0)

		self.assertEqual(self.out.readlines()[-1].strip(), "Result_exam created(ID: %d)" % result_exam.id)

		result_exam.valuetion = 4
		result_exam.save()

		self.out.seek(0)

		self.assertEqual(self.out.readlines()[-1].strip(), "Result_exam updated(ID: %d)" % result_exam.id)

	def test_log_result_exam_delete(self):
		res_exam = Result_exam(valuetion=5)
		res_exam.save()
		
		ruid = res_exam.id
		res_exam.delete()

		self.out.seek(0)

		self.assertEqual(self.out.readlines()[-1].strip(), "Result_exam deleted(ID: %d)" % ruid)

	def test_log_result_exam_change_students(self):
		res_exam = Result_exam(valuetion=5)
		res_exam.save()
		student = Student(first_name='Ioan', last_name='Serok')
		student.save()
		res_exam.students.add(student)
		res_exam.save()

		self.out.seek(0)

		self.assertEqual(self.out.readlines()[-2].strip(), "List of students was modified \
					 in result_exam {}".format(res_exam.id))
