# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.urlresolvers import reverse

from ..models.Group import Group

from django.views.generic import DeleteView


# Views for Groups
def groups_list(request):
	groups = Group.objects.all()
	allGroups = len(groups)
	valGroupsOnPage = int(request.GET.get('valgroups', 3))
	valPage = allGroups/valGroupsOnPage
	
	if allGroups % valGroupsOnPage != 0:
		valPage += 1
	listOfPage = [str(i) for i in xrange(1, valPage+1, 1)]

	order_by = request.GET.get('order_by', '')
	if order_by in ('id', 'title', 'leader'):
		groups = groups.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
				groups = groups.reverse()

	# paginator groups
	# paginator = Paginator(groups, 3)
	# page = request.GET.get('page')
	# try:
	# 	groups = paginator.page(page)
	# except PageNotAnInteger:
	# 	# If page is not an integer, deliver first page.
	# 	groups = paginator.page(1)
	# except EmptyPage:
	# 	# If page is out of range (e. g. 9999), deliver
	# 	# last page of results.
	# 	groups = paginator.page(paginator.num_pages)

	# my paginator groups
	page = request.GET.get('page', '')
	
	try:
		page = int(float(page))
	except ValueError:
		page = 1
	if page > valPage or page < 1:
		page = valPage
	
	large = valGroupsOnPage*page
	little = large - valGroupsOnPage
	if allGroups > 1:
		groups = groups[little:large]

	return render(request, 'students/groups_list.html', {'groups': groups,
														 'valPage': valPage,
														 'listOfPage': listOfPage})

def groups_add(request):
	return HttpResponse('<h1>Groups Add Form</h1>')

def groups_edit(request, gid):
	return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
	return HttpResponse('<h1>Delete Group %s</h1>' % gid)

class GroupDeleteView(DeleteView):
	"""docstring for GroupDeleteView"""
	model = Group
	template_name = 'students/groups_confirm_delete.html'
	pk_url_kwarg = 'gid'
	
	def get_success_url(self):
		messages.success(self.request, u'Групу %s успішно видалено!' % self.object)
		return reverse('home')
