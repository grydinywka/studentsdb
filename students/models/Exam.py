from django.db import models
from django.utils.translation import ugettext_lazy as _

class Exam(models.Model):
	"""Exams Model"""

	class Meta(object):	
		verbose_name = _(u"Exam")
		verbose_name_plural = _(u"Exams")

	title = models.CharField(
		max_length=256,
		blank=False,
		verbose_name=_(u"Title"))
	
	exam_date = models.DateTimeField(
		blank=False,
		verbose_name=_(u"Date and time of exam"),
		null=True)

	presenter = models.CharField(
		max_length=256,
		blank=False,
		verbose_name=_(u"Presenter"))

	exam_group = models.ManyToManyField('Group',
		verbose_name=_(u"Groups for exam"),
		blank=True,
		related_name='exams')

	notes = models.TextField(
		blank=True,
		verbose_name=_(u"Notes"))
	
	def __unicode__(self):
		return u"%s" % (self.title,)
