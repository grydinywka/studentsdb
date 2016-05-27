from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_value(value):
	if value < 0 or value > 10:
		raise ValidationError(_(u'%s does not belong to range from zero to ten!') % value)

# Create your models here.
class Result_exam(models.Model):
	"""Result Model"""

	class Meta(object):
		verbose_name = _(u"Result")
		verbose_name_plural = _(u"Results")
	
	valuetion = models.DecimalField(
		max_digits=2,
		decimal_places=0,
		blank=False,
		verbose_name=_(u"Valuetion"),
		validators=[validate_value])

	students = models.ManyToManyField('Student',
		verbose_name=_(u"Students"),
		blank=False)
	
	exams = models.ManyToManyField('Exam',
		blank=False,
		verbose_name=_(u"Exams"))
	
	notes = models.TextField(
		blank=True,
		verbose_name=_(u"Notes"))

	def __unicode__(self):
		# listofStud = self.students.all()
		return u"%s" % (self.valuetion)

Result_exam.validate_value = validate_value
