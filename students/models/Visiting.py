from django.db import models
from django.utils.translation import ugettext_lazy as _

class Visiting(models.Model):
	"""Visit's Model"""

	class Meta(object):	
		verbose_name = _(u"Visiting")
		verbose_name_plural = _(u"All Visiting")

	title = models.CharField(
		max_length=256,
		blank=False,
		verbose_name=_(u"Title"))
	
	def __unicode__(self):
		if True:
			return u"%s" % (self.title)
		else:
			return u"%s" % (self.title,)
