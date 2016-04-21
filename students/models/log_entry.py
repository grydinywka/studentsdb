# -*- coding: utf-8 -*-

from django.db import models

class LogEntry(models.Model):
	level = models.CharField(
		max_length=20,
		blank=False,
		verbose_name='Level')
	asctime = models.DateTimeField(
		blank=False,
		verbose_name='Date and time event',
		null=True)
	module = models.CharField(
		max_length=100,
		blank=False,)
	message = models.TextField(
		blank=False,)
	def __unicode__(self):
		return u"%s %s %s %s" % (self.level, self.asctime, self.module, self.message)
