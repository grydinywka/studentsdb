from .util import get_groups, get_custom_language

def groups_processor(request):
	return {'GROUPS': get_groups(request)}

def language_processor(request):
	get_custom_language(request)
	return {'LANG': request.COOKIES.has_key('cust_lang') and request.COOKIES['cust_lang'] or False}