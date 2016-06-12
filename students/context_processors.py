from .util import get_groups
from django.conf import settings

def groups_processor(request):
	return {'GROUPS': get_groups(request)}

def lang_cookie_name(request):
	return {'LANGUAGE_COOKIE_NAME': request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, '')}