from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.views.i18n import javascript_catalog
from django.views.generic.base import RedirectView

from django.contrib.auth.decorators import login_required

from .settings import MEDIA_ROOT, DEBUG

from students.views.students import StudentList, StudentUpdateView,\
                                    StudentEditView, StudentAddView,\
                                    StudentDeleteView, students_delete_mult
from students.views.students import StudentDeleteView2
from students.views.groups import GroupList, GroupDeleteView,\
                                  GroupEditView, GroupAddView,\
                                  groups_edit_handle, groups_delete_handle

from students.views.journal import JournalView
from students.views.exams import ExamList, ExamEditView,\
                                 ExamAddView, ExamDeleteView,\
                                 exams_confirm_delete_handle
from students.views.results import result_list
from students.views.contact_admin2 import ContactView
from students.views.contact_admin import ContactView2

from students.views.log_entry import LogEntryList

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('students',),
}

urlpatterns = patterns('',
    # Students urls
    # url(r'^$', 'students.views.students.students_list', name='home'),
    url(r'^$', StudentList.as_view(), name='home'),
    
    # url(r'^students/add/$', 'students.views.students.students_add2', name='students_add'),
    # url(r'^students/add/$', 'students.views.students.students_add', name='students_add'),
    url(r'^students/add/$', StudentAddView.as_view(), name='students_add'),
    
    url(r'^students/(?P<sid>\d+)/edit/$', StudentEditView.as_view(), name="students_edit"),
    # url(r'^students/(?P<sid>\d+)/edit/$', StudentUpdateView.as_view(), name="students_edit"),
   
    # url(r'^students/(?P<sid>\d+)/delete/$', StudentDeleteView.as_view(), name='students_delete'),
    url(r'^students/(?P<sid>\d+)/delete/$', StudentDeleteView2.as_view(), name='students_delete'),
    # url(r'^students/(?P<sid>\d+)/delete/$', 'students.views.students.students_delete2', name='students_delete'),
    url(r'^students/delete_mult/$', students_delete_mult, name='students_delete_mult'),
    
    url(r'^student_list/$', StudentList.as_view()),
    url(r'^student_list/(?P<pk>\d+)/$', StudentList.as_view()),
    
    # Groups urls
    # url(r'^groups/$', 'students.views.groups.groups_list', name='groups'),
    url(r'^groups/$', GroupList.as_view(), name='groups'),
    
    # url(r'^groups/add/$', 'students.views.groups.groups_add_handle', name='groups_add'),
    # url(r'^groups/add/$', 'students.views.groups.groups_add_django_form', name='groups_add'),
    url(r'^groups/add/$', login_required(GroupAddView.as_view()), name='groups_add'),
    
    url(r'^groups/(?P<gid>\d+)/edit/$', login_required(groups_edit_handle), name='groups_edit'),
    # url(r'^groups/(?P<gid>\d+)/edit/$', GroupEditView.as_view(), name='groups_edit'),

    # url(r'^groups/(?P<gid>\d+)/delete/$', GroupDeleteView.as_view(), name='groups_delete'),
    url(r'^groups/(?P<gid>\d+)/delete/$', login_required(groups_delete_handle), name='groups_delete'),
    
    # Journal urls
    url(r'^journal/(?P<pk>\d+)?/?$', login_required(JournalView.as_view()), name='journal'),
    url(r'^journal2/$', 'students.views.journals.journal_list', name='journal2'),
    # url(r'^journal2/$', 'students.views.journals.data_requests'),
    url(r'^journal2/(?P<gid>\d+)/edit/$', 'students.views.journal_edit.journal_edit', name="journal_edit"),
    url(r'^journal/group/(?P<group_pk>\d+)/$', login_required(JournalView.as_view()), name='journal_group'),

    # Exam urls
    # url(r'^exams/$', 'students.views.exams.exams_list', name='exams'),
    url(r'^exams/$', login_required(ExamList.as_view()), name='exams'),

    # url(r'^exams/(?P<eid>\d+)/edit/$', 'students.views.exams.exams_edit_django_form', name='exams_edit'),
    # url(r'^exams/(?P<eid>\d+)/edit/$', 'students.views.exams.exams_edit_handle', name='exams_edit'),
    url(r'^exams/(?P<eid>\d+)/edit/$', login_required(ExamEditView.as_view()), name='exams_edit'),

    # url(r'^exams/add/$', 'students.views.exams.exams_add_handle', name='exams_add'),
    url(r'^exams/add/$', login_required(ExamAddView.as_view()), name='exams_add'),

    url(r'^exams/(?P<eid>\d+)/delete/$', login_required(exams_confirm_delete_handle), name='exams_delete'),
    # url(r'^exams/(?P<eid>\d+)/delete/$', ExamDeleteView.as_view(), name='exams_delete'),

    # Result urls
    url(r'^result/$', login_required(result_list), name='results'),

    #Contact Admin Form
    # url(r'^contact-admin/$', 'students.views.contact_admin2.contact_admin', name='contact_admin'),
    url(r'^contact-admin/$', ContactView.as_view(), name='contact_admin'),
    (r'^contact/', include('contact_form.urls')),
    url(r'^contact2/$', ContactView2.as_view(), name='contact2'),

    url(r'^log-entry/$', login_required(LogEntryList.as_view()), name='log'),

    url(r'^jsi18n\.js$', javascript_catalog, js_info_dict, name="javascript-catalog"),

    url(r'^counts/$', 'students.views.students.count_apple', name="count"),

    url(r'^get-lang-cookie-name/$', 'students.util.get_language_cookie_name', name='get_language_cookie_name'),

    # User Related urls
    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'}, name='auth_logout'),
    url(r'^register/complete/$', RedirectView.as_view(pattern_name='home'), name='registration_complete'),
    url(r'^users/', include('registration.backends.simple.urls', namespace='users')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

if DEBUG:
    # serve files from media folder
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': MEDIA_ROOT}))
