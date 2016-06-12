from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.conf import settings

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
	if allStudents <= valStudOnPage and allStudents > 0:
		valStudOnPage = allStudents
	valPage = allStudents/valStudOnPage
	valStudOnLastPage = allStudents % valStudOnPage
	if valStudOnLastPage != 0:
		valPage += 1

	page = request.GET.get('page', 1)
	try:
		page = int(float(page))
	except ValueError:
		page = 1
	if page > valPage:
		page = valPage
	if  page < 1:
		page = 1

	if page == valPage:
		large = allStudents
		if valStudOnLastPage > 0:
			little = large - valStudOnLastPage
		else:
			little = large - valStudOnPage
	else:
		large = valStudOnPage*page
		little = large - valStudOnPage

	if little < 0:
		little = 0
	if large < 0:
		large = 0

	return little, large

def get_groups(request):
	"""Returns list of existing groups"""
	# deferred import of Group model to avoid cycled imports
	from .models import Group

	# get currently selected group
	cur_group = get_current_group(request)

	groups = []
	for group in Group.objects.all().order_by('title'):
		groups.append({
			'id': group.id,
			'title': group.title,
			'leader': group.leader and (u'%s %s' % (group.leader.first_name, group.leader.last_name)) or None,
			'selected': cur_group and cur_group.id == group.id and True or False
		})

	return groups

def get_current_group(request):
	"""Returns currently selected group or None"""

	# we remember selected group in a cookie
	pk = request.COOKIES.get('current_group')

	if pk:
		from .models import Group
		try:
			group = Group.objects.get(pk=int(pk))
		except Group.DoesNotExist:
			return None
		except TypeError:
			return None
		else:
			return group
	else:
		return None

def get_language_cookie_name(request):
	lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
	response_dict = {'django_lang': ''}
	
	if lang:
		import logging
		try:
			response_dict['django_lang'] = settings.LANGUAGE_COOKIE_NAME
		except Exception as e:
			logger = logging.getLogger(__name__)
			logger.exception('Error during setting language. Was tried {} language'.format(lang))
		else:
			logger = logging.getLogger(__name__)
			logger.info('Was set {} language'.format(lang))

	return JsonResponse(response_dict, safe=False)

