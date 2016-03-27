# -*- coding: utf-8 -*-
from django.db import models

# def getInstance(mjClass, *args):
# 	mj = mjClass
# 	limit = 32
# 	for day in xrange(1, limit, 1):
# 		setattr(mj, "present_day%s" % day, models.BooleanField(default=False))
# 	return mj(*args)

# def myDecor(mjClass, *args):
# 	def onCall(*args):
# 		return getInstance(mjClass, *args)
# 	return onCall

class MonthJournal(models.Model):
	"""Student Monthly Journal"""

	class Meta:
		verbose_name = u'Місячний Журнал'
		verbose_name_plural = u'Місячні Журнали'

	student = models.ForeignKey('Student',
		verbose_name=u'Студент',
		blank=False,
		unique_for_month='date')
		
	# we only need year and month, so always set day ofthe month
	date = models.DateField(
		verbose_name=u'Дата',
		blank=False)

	scope = locals()
	for item in xrange(1, 32, 1):
		scope['present_day' + str(item)] = models.BooleanField(verbose_name = u'День №'+str(item), default=False)
	
	# list of days, each says whether student  was presented or not
	# present_day1 = models.BooleanField(default=False)
	# present_day2 = models.BooleanField(default=False)
	# present_day3 = models.BooleanField(default=False)
	# present_day4 = models.BooleanField(default=False)
	# present_day5 = models.BooleanField(default=False)
	# present_day6 = models.BooleanField(default=False)
	# present_day7 = models.BooleanField(default=False)
	# present_day8 = models.BooleanField(default=False)
	# present_day9 = models.BooleanField(default=False)
	# present_day10 = models.BooleanField(default=False)
	# present_day11 = models.BooleanField(default=False)
	# present_day12 = models.BooleanField(default=False)
	# present_day13 = models.BooleanField(default=False)
	# present_day14 = models.BooleanField(default=False)
	# present_day15 = models.BooleanField(default=False)
	# present_day16 = models.BooleanField(default=False)
	# present_day17 = models.BooleanField(default=False)
	# present_day18 = models.BooleanField(default=False)
	# present_day19 = models.BooleanField(default=False)
	# present_day20 = models.BooleanField(default=False)
	# present_day21 = models.BooleanField(default=False)
	# present_day22 = models.BooleanField(default=False)
	# present_day23 = models.BooleanField(default=False)
	# present_day24 = models.BooleanField(default=False)
	# present_day25 = models.BooleanField(default=False)
	# present_day26 = models.BooleanField(default=False)
	# present_day27 = models.BooleanField(default=False)
	# present_day28 = models.BooleanField(default=False)
	# present_day29 = models.BooleanField(default=False)
	# present_day30 = models.BooleanField(default=False)
	# present_day31 = models.BooleanField(default=False)
	
	def __unicode__(self):
		return u'Student %s: Month:%d, Year:%d' % (self.student.last_name, self.date.month, self.date.year)

# limit = 32
# for day in xrange(1, limit, 1):
# 	setattr(MonthJournal, "present_day%s" % day, models.BooleanField(default=False))
