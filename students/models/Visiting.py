# -*- coding: utf-8 -*-

from django.db import models

class Visiting(models.Model):
	"""Visit's Model"""

	class Meta(object):	
		verbose_name = u"Відвідування"
		verbose_name_plural = u"Усі відвідування"

	title = models.CharField(
		max_length=256,
		blank=False,
		verbose_name=u"Назва")

	group = models.OneToOneField('Group',
		blank=True,
		null=True,
		verbose_name=u"Відвідини в група",
		on_delete=models.SET_NULL)
	
	def __unicode__(self):
		if self.group:
			return u"%s (%s)" % (self.title, self.group.title)
		else:
			return u"%s" % (self.title,)
