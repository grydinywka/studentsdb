# -*- coding: utf-8 -*-

import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Student, Group, MonthJournal

@receiver(post_save, sender=Student)
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
