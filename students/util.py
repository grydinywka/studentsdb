from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate(objects, size, request, context, var_name='object_list'):
	"""Paginate objects provided by view.

	THis function takes:
		* list of elements;
		* number of objects per page;
		* request object to get url paramerers from;
		* context to set new variables into;
		* var_name = variable name for list of objects.

	It returns updated context object.
	"""
	# apply pagination
	paginator = Paginator(objects, size)

	# try to get page number from request
	page = request.GET.get('page', '1')
	try:
		object_list = paginator.page(page)
	except PageNotAnInteger:
		# if page is not an integer, deliver first page
		object_list = paginator.page(1)
	except EmptyPage:
		# if page is out of range (e.g. 9999),
		# deliver last page of results
		object_list = paginator.page(paginator.num_pages)

	# set variables into context
	context[var_name] = object_list
	context['is_paginated'] = object_list.has_other_pages()
	context['page_obj'] = object_list
	context['paginator'] = paginator

	return context

def boundsStuds(objects, valStudOnPage, request):
	allStudents = len(objects)
	if allStudents <= valStudOnPage:
		valStudOnPage = allStudents
	valPage = allStudents/valStudOnPage
	if allStudents % valStudOnPage != 0:
		valPage += 1

	page = request.GET.get('page', 1)
	try:
		page = int(float(page))
	except ValueError:
		page = 1
	if page > valPage or page < 1:
		page = valPage

	if page == valPage:
		large = allStudents
		little = allStudents - allStudents % valStudOnPage
	else:
		large = valStudOnPage*page
		little = large - valStudOnPage

	return little, large
