# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import logging

from django.db.models.signals import post_save, post_delete, m2m_changed, pre_delete
from django.db.models.signals import post_migrate

from django.core.signals import request_started, request_finished

from django.dispatch import receiver, Signal

from .models import Student, Group, MonthJournal, Exam, Result_exam, DayCounterRequest

from datetime import date

request_counter = 0

def log_student_updated_added_event(sender, **kwargs):
	"""Writes information about newly added or updated student info log file"""
	logger = logging.getLogger(__name__)

	student = kwargs['instance']
	if kwargs['created']:
		logger.info("Student added: %s %s (ID: %d)", student.first_name,
													 student.last_name,
													 student.id)
	else:
		logger.info("Student updated: %s %s (ID: %d)", student.first_name,
													   student.last_name,
													   student.id)
post_save.connect(log_student_updated_added_event, sender=Student)

@receiver(post_delete, sender=Student)
def log_student_deleted_event(sender, **kwargs):
	"""Writes information about deleted student into log file"""
	logger = logging.getLogger(__name__)

	student = kwargs['instance']
	logger.info("Student deleted: %s %s (ID: %d)", student.first_name,
												   student.last_name,
												   student.id)

@receiver(post_save, sender=Group)
def log_group_edit_add_event(sender, **kwargs):
	"""Log after edit or add group"""
	logger = logging.getLogger(__name__)

	group = kwargs['instance']
	if kwargs['created']:
		logger.info("Group added: %s (ID: %d)", group.title, group.id)
	else:
		logger.info("Group edited: %s (ID: %d)", group.title, group.id)

@receiver(post_delete, sender=Group)
def log_group_delete_event(sender, **kwargs):
	logger = logging.getLogger(__name__)

	group = kwargs['instance']
	logger.info("Group deleted: %s (ID: %d)", group.title, group.id)

@receiver(post_save, sender=MonthJournal)
def log_journal_update_add_event(sender, **kwargs):
	logger = logging.getLogger(__name__)

	monthjournal = kwargs['instance']
	if kwargs['created']:
		logger.info("MonthJournal created: %s", monthjournal)
	else:
		logger.info("MonthJournal updated: %s", monthjournal)

@receiver(post_delete, sender=MonthJournal)
def log_journal_delete_event(sender, **kwargs):
	logger = logging.getLogger(__name__)

	monthjournal = kwargs['instance']
	logger.info("MonthJournal deleted: %s", monthjournal)

@receiver(post_save, sender=Exam)
def log_exam_add_update_event(sender, **kwargs):
	logger = logging.getLogger(__name__)

	exam = kwargs['instance']
	
	if kwargs['created']:
		logger.info("Exam created: %s (ID: %d)", exam.title, exam.id)
	else:
		logger.info("Exam updated: %s (ID: %d)", exam.title, exam.id)

def log_group_of_exam_update_event(sender, **kwargs):
	logger = logging.getLogger(__name__)

	exam = kwargs['instance']
	action = kwargs['action']

	if action == "post_add":
		info_str = "exam {} have next groups after modified:\n".format(exam)
		for item in kwargs["pk_set"]:
			group = kwargs["model"].objects.filter(pk=item)[0]
			info_str += group.title + '\n'
		logger.info(info_str)	
m2m_changed.connect(log_group_of_exam_update_event, sender=Exam.exam_group.through)

@receiver(post_delete, sender=Exam)
def log_exam_delete_event(sender, **kwargs):
	logger = logging.getLogger(__name__)

	exam = kwargs['instance']
	logger.info("Exam deleted: %s", exam)

@receiver(post_delete, sender=Result_exam)
def log_resultexam_delete_event(sender, **kwargs):
	logger = logging.getLogger(__name__)

	result_exam = kwargs['instance']
	logger.info("Result_exam deleted(ID: %d)", result_exam.id)

@receiver(post_save, sender=Result_exam)
def log_resultexam_add_update_event(sender, **kwargs):
	logger = logging.getLogger(__name__)

	result_exam = kwargs['instance']
	if kwargs['created']:
		logger.info("Result_exam created(ID: %d)", result_exam.id)
	else:
		logger.info("Result_exam updated(ID: %d)", result_exam.id)

@receiver(m2m_changed, sender=Result_exam.students.through)
def log_resultexam_change_list_stud_event(sender, **kwargs):
	logger = logging.getLogger(__name__)
	result_exam = kwargs['instance']

	if kwargs['action'] == 'post_add':
		logger.info("List of students was modified \
					 in result_exam {}".format(result_exam.id))

# bellow will be custom signal
contact_admin_signal = Signal(providing_args=[])

def contact_admin_handler(sender, **kwargs):
	logger = logging.getLogger('contact_admin_logger')
	logger.info("My custom handler for contact admin form.")

contact_admin_signal.connect(contact_admin_handler)

# handler for requests
def counter_start_request(sender, **kwargs):
	f = open('/data/work/virtualenvs/studDb/src/studDb/students/counter_file.txt', 'r+')
	counter = int(f.readline()) + 1
	f.seek(0)
	f.write(str(counter))
	f.close()
	
	logger = logging.getLogger('django.request')
	logger.info("request #{}".format(counter))
request_started.connect(counter_start_request)

@receiver(post_migrate)
def all_migrate_command(sender, **kwargs):
	logger = logging.getLogger(__name__)
	db_info = kwargs['using']
	app_config_label = kwargs['app_config'].label

	logger.info("Here is used {} database! App: {}".format(db_info, app_config_label))
