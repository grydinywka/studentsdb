from django.shortcuts import render
from django.http import HttpResponse

# Views for Students
def students_list(request):
	#import pdb;pdb.set_trace()
	# template = loader.get_template('demo.html')
	# context = RequestContext(request, {})
	# return HttpRespose(template.render(context))
	
	return render(request, 'students/students_list.html', {})
	
	#return HttpResponse('<h1>Hello World!</h1>')

def students_add(request):
    return HttpResponse('<h1>Students Add Form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)

# Views for Gruops
def groups_list(request):
    return HttpResponse('<h1>Groups Listing!</h1>')

def groups_add(request):
    return HttpResponse('<h1>Groups Add Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)
