# -*- coding: utf-8 -*-

from django.db import models

class DayCounterRequest(models.Model):
	"""Request's value a day"""

	class Meta:
		verbose_name = u'Добовий лічильник запитів'
		verbose_name_plural = u'Добові лічильники запитів'

	date = models.DateField(
		verbose_name=u'Дата',
		blank=False,
		unique=True
	)
	counter = models.IntegerField(
		verbose_name=u'Лічильник',
		blank=False,
		default=1
	)
	def __unicode__(self):
		return u"%s, requests' values %s" % (self.date, self.counter)
