from django.db import models
from django.utils.translation import ugettext_lazy as _

class LogEntry(models.Model):
	level = models.CharField(
		max_length=20,
		blank=False,
		verbose_name=_(u'Level'))
	asctime = models.DateTimeField(
		blank=False,
		verbose_name=_(u'Date and time event'),
		null=True)
	module = models.CharField(
		max_length=100,
		blank=False,)
	message = models.TextField(
		blank=False,)
	def __unicode__(self):
		return u"%s %s %s %s" % (self.level, self.asctime, self.module, self.message)
