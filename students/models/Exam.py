# -*- coding: utf-8 -*-

from django.db import models

class Exam(models.Model):
	"""Exams Model"""

	class Meta(object):	
		verbose_name = u"Іспит"
		verbose_name_plural = u"Іспити"

	title = models.CharField(
		max_length=256,
		blank=False,
		verbose_name=u"Назва")
	
	exam_date = models.DateTimeField(
		blank=False,
		verbose_name=u"Дата і час іспиту",
		null=True)

	presenter = models.CharField(
		max_length=256,
		blank=False,
		verbose_name=u"Екзаменатор")

	exam_group = models.ManyToManyField('Group',
		verbose_name=u"Група для іспиту",
		blank=True,
		null=True,
		related_name='exams')

	notes = models.TextField(
		blank=True,
		verbose_name=u"Додаткові нотатки")
	
	def __unicode__(self):
		return u"%s" % (self.title,)
