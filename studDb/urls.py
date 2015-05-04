from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .settings import MEDIA_ROOT, DEBUG

urlpatterns = patterns('',
    # Students urls
    url(r'^$', 'students.views.students.students_list', name='home'),
    url(r'^students/add/$', 'students.views.students.students_add', name='students_add'),
    url(r'^students/(?P<sid>\d+)/edit/$', 'students.views.students.students_edit', name='students_edit'),
    url(r'^students/(?P<sid>\d+)/delete/$', 'students.views.students.students_delete', name='students_delete'),
    
    # Groups urls
    url(r'^groups/$', 'students.views.groups.groups_list', name='groups'),
    
    url(r'^groups/add/$', 'students.views.groups.groups_add', name='groups_add'),
    
    url(r'^groups/(?P<gid>\d+)/edit/$', 'students.views.groups.groups_edit', name='groups_edit'),
    
    url(r'^groups/(?P<gid>\d+)/delete/$', 'students.views.groups.groups_delete', name='groups_delete'),
    
    # Journal urls
    url(r'^journal/$', 'students.views.journals.journal_list', name='journal'),
    url(r'^journal/(?P<gid>\d+)/edit/$', 'students.views.journal_edit.journal_edit', name="journal_edit"),

    # Exam urls
    url(r'^exam/$', 'students.views.exams.exam_list', name='exams'),
    url(r'^exam/(?P<gid>\d+)/edit/$', 'students.views.exams.exam_edit', name='exam_edit'),

    # Result urls
    url(r'^result/$', 'students.views.results.result_list', name='results'),

    #Contact Admin Form
    url(r'^contact-admin/$', 'students.views.contact_admin.contact_admin', name='contact_admin'),
    
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

if DEBUG:
    # serve files from media folder
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': MEDIA_ROOT}))
