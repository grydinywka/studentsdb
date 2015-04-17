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
	
	def __unicode__(self):
		if True:
			return u"%s" % (self.title)
		else:
			return u"%s" % (self.title,)
