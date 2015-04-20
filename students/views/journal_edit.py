# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
import datetime

from ..models.Visiting import Visiting

def getMonth(date):
	mon_list = []
	one_day = datetime.timedelta(days=1)
	next_month = date.month + 1

	while date.month < next_month:
		mon_list.append(date)
		date += one_day

	return mon_list

def getDaysList(month_list):
	days_list = []

	for date in month_list:
		day = date.strftime("%A")[:2]
		days_list.append(day)

	return days_list

# def getNextDate(d):
# 	year = d.year
# 	month = d.month
# 	if month == 12:
# 		year += 1
# 		month = 1
# 	else:
# 		month += 1
# 	newDate = datetime.date(year, month, 1)

# 	return newDate

def journal_edit(request, gid):
	visiting = Visiting.objects.get(id=gid)
	# visiting = Visiting.objects.all()[int(gid)-1].student_set.all()
	month = int(request.GET.get('month', '9'))
	year = int(request.GET.get('year', '2014'))
	d1 = datetime.date(2014, 9, 1)
	month_list = getMonth(d1)
	month_day_week_list = getDaysList(month_list)
	# next_date = getNextDate(d1)
	# previous_date = getPreDate(month, year)

	

	# return HttpResponse('<h1>Here will be journal of students!</h1>')
	return render(request, 'students/journal_edit.html', {'visiting': visiting,
													  'monthDate': month_list,
													  'days': month_day_week_list,
													  'date': d1.strftime("%B") + ' ' + d1.strftime("%Y")})
													  # 'next_date': next_date
													  


# d1 = datetime.date(2014, 12, 1)
# d2 = getNextDate(d1)
# print d2
# month_list = getMonth(d1)
# month_day_week_list = getDaysList(month_list)

# for day, date in zip(month_day_week_list, month_list):
# 	print day + ': ' + str(date)
