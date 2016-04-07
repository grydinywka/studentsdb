# -*- coding: utf-8 -*-

from django.db import models
from django.core.exceptions import ValidationError

def validate_value(value):
	if value < 0 or value > 10:
		raise ValidationError(u'%s does not belong to range from zero to ten!' % value)

# Create your models here.
class Result_exam(models.Model):
	"""Result Model"""

	class Meta(object):
		verbose_name = u"Результат"
		verbose_name_plural = u"Результати"
	
	valuetion = models.DecimalField(
		max_digits=2,
		decimal_places=0,
		blank=False,
		verbose_name=u"Оцінка",
		validators=[validate_value])

	students = models.ManyToManyField('Student',
		verbose_name=u"Студент",
		blank=False)
	
	exams = models.ManyToManyField('Exam',
		blank=False,
		verbose_name=u"Іспит")
	
	notes = models.TextField(
		blank=True,
		verbose_name=u"Додаткові нотатки")

	def __unicode__(self):
		# listofStud = self.students.all()
		return u"%s" % (self.valuetion)

Result_exam.validate_value = validate_value
