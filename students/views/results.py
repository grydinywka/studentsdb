from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from ..models.Result_exam import Result_exam

def result_list(request):
	results = Result_exam.objects.all()
	order_by = request.GET.get('order_by', '')
	if order_by in ('id',):
		results = results.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			results = results.reverse()
	
	return render(request, 'students/result_list.html', {'results': results})
	# return HttpResponse('<h1>It is a first result:</h1>')
