# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

# Views for Students
def students_list(request):
	#import pdb;pdb.set_trace()
	# template = loader.get_template('demo.html')
	# context = RequestContext(request, {})
	# return HttpRespose(template.render(context))
	students = (
		{'id': 1,
		 'first_name': u'Андрій',
		 'last_name': u'Корост',
		 'ticket': 2123,
		 'image': 'img/Foto,pajalka.JPG'},
		{'id': 2,
		 'first_name': u'Сергій',
		 'last_name': u'Ігнатенко',
		 'ticket': 1221,
		 'image': 'img/P1014486.JPG'},
		{'id': 3,
		 'first_name': u'Мік',
		 'last_name': u'Джагер',
		 'ticket': 1122,
		 'image': 'img/c.jpg'},
	)
	
	return render(request, 'students/students_list.html', {'students': students})
	
	# return HttpResponse('<h1>Hello World!</h1>')

def students_add(request):
    return HttpResponse('<h1>Students Add Form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)

# Views for Gruops
def groups_list(request):
	groups = (
		{'id': 1,
		 'name': [u'МтМ-', 21],
		 'captain': u'Ячменев Олег'},
		{'id': 2,
		 'name': [u'МтМ-', 22],
		 'captain': u'Подоба Віталій'},
		{'id': 3,
		 'name': [u'МтМ-', 23],
		 'captain': u'Іванов Андрій'},
	)
	
	# return render(request, 'students/groups_list.html', {})
	return render(request, 'students/groups_list.html', {'groups': groups})

def groups_add(request):
    return HttpResponse('<h1>Groups Add Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)
