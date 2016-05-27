from django.db import models
from django.utils.translation import ugettext_lazy as _

class DayCounterRequest(models.Model):
	"""Request's value a day"""

	class Meta:
		verbose_name = _(u'Daily counter of requests')
		verbose_name_plural = _(u'Dailies counters of requests')

	date = models.DateField(
		verbose_name=_(u'Date'),
		blank=False,
		unique=True
	)
	counter = models.IntegerField(
		verbose_name=_(u'Counter'),
		blank=False,
		default=0
	)
	def __unicode__(self):
		return u"%s, requests' values %s" % (self.date, self.counter)
