from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .settings import MEDIA_ROOT, DEBUG

from students.views.students import StudentList, StudentUpdateView, StudentEditView, StudentAddView, StudentDeleteView
from students.views.students import StudentDeleteView2
from students.views.groups import GroupList, GroupDeleteView, GroupEditView, GroupAddView
from students.views.journal import JournalView
from students.views.exams import ExamList, ExamEditView, ExamAddView, ExamDeleteView
from students.views.contact_admin2 import ContactView
from students.views.contact_admin import ContactView2

urlpatterns = patterns('',
    # Students urls
    # url(r'^$', 'students.views.students.students_list', name='home'),
    url(r'^$', StudentList.as_view(), name='home'),
    
    # url(r'^students/add/$', 'students.views.students.students_add2', name='students_add'),
    url(r'^students/add/$', StudentAddView.as_view(), name='students_add'),
    
    # url(r'^students/(?P<sid>\d+)/edit/$', 'students.views.students.students_edit', name='students_edit'),
    # url(r'^students/(?P<sid>\d+)/edit/$', 'students.views.students.students_edit2', name='students_edit'),
    url(r'^students/(?P<sid>\d+)/edit/$', StudentEditView.as_view(), name="students_edit"),
    # url(r'^students/(?P<sid>\d+)/edit/$', StudentUpdateView.as_view(), name="students_edit"),
   
    # url(r'^students/(?P<sid>\d+)/delete/$', StudentDeleteView.as_view(), name='students_delete'),
    url(r'^students/(?P<sid>\d+)/delete/$', StudentDeleteView2.as_view(), name='students_delete'),
    # url(r'^students/(?P<sid>\d+)/delete/$', 'students.views.students.students_delete2', name='students_delete'),
    url(r'^students/delete_mult/$', 'students.views.students.students_delete_mult', name='students_delete_mult'),
    
    url(r'^student_list/$', StudentList.as_view()),
    url(r'^student_list/(?P<pk>\d+)/$', StudentList.as_view()),
    
    # Groups urls
    # url(r'^groups/$', 'students.views.groups.groups_list', name='groups'),
    url(r'^groups/$', GroupList.as_view(), name='groups'),
    
    # url(r'^groups/add/$', 'students.views.groups.groups_add_handle', name='groups_add'),
    # url(r'^groups/add/$', 'students.views.groups.groups_add_django_form', name='groups_add'),
    url(r'^groups/add/$', GroupAddView.as_view(), name='groups_add'),
    
    url(r'^groups/(?P<gid>\d+)/edit/$', 'students.views.groups.groups_edit_handle', name='groups_edit'),
    # url(r'^groups/(?P<gid>\d+)/edit/$', GroupEditView.as_view(), name='groups_edit'),

    # url(r'^groups/(?P<gid>\d+)/delete/$', GroupDeleteView.as_view(), name='groups_delete'),
    url(r'^groups/(?P<gid>\d+)/delete/$', 'students.views.groups.groups_delete_handle', name='groups_delete'),
    
    # Journal urls
    url(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(), name='journal'),
    # url(r'^journal/$', 'students.views.journals.journal_list', name='journal'),
    # url(r'^journal/(?P<gid>\d+)/edit/$', 'students.views.journal_edit.journal_edit', name="journal_edit"),

    # Exam urls
    # url(r'^exams/$', 'students.views.exams.exams_list', name='exams'),
    url(r'^exams/$', ExamList.as_view(), name='exams'),

    # url(r'^exams/(?P<eid>\d+)/edit/$', 'students.views.exams.exams_edit_django_form', name='exams_edit'),
    # url(r'^exams/(?P<eid>\d+)/edit/$', 'students.views.exams.exams_edit_handle', name='exams_edit'),
    url(r'^exams/(?P<eid>\d+)/edit/$', ExamEditView.as_view(), name='exams_edit'),

    # url(r'^exams/add/$', 'students.views.exams.exams_add_handle', name='exams_add'),
    url(r'^exams/add/$', ExamAddView.as_view(), name='exams_add'),

    url(r'^exams/(?P<eid>\d+)/delete/$', 'students.views.exams.exams_confirm_delete_handle', name='exams_delete'),
    # url(r'^exams/(?P<eid>\d+)/delete/$', ExamDeleteView.as_view(), name='exams_delete'),

    # Result urls
    url(r'^result/$', 'students.views.results.result_list', name='results'),

    #Contact Admin Form
    # url(r'^contact-admin/$', 'students.views.contact_admin2.contact_admin', name='contact_admin'),
    url(r'^contact-admin/$', ContactView.as_view(), name='contact_admin'),
    (r'^contact/', include('contact_form.urls')),
    url(r'^contact2/$', ContactView2.as_view(), name='contact2'),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

if DEBUG:
    # serve files from media folder
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': MEDIA_ROOT}))
