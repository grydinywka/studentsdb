# -*- coding: utf-8 -*-

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError

from .models.Student import Student
from .models.Group import Group
from .models.Visiting import Visiting
from .models.Exam import Exam
from .models.Result_exam import Result_exam
from .models.monthjournal import MonthJournal #, Singleton

class StudentFormAdmin(ModelForm):

	def clean_student_group(self):
		"""Check if student is leader in any group.

		If yes? then ensure it's the same as selected group."""
		# get group where current student is a leader
		groups = Group.objects.filter(leader=self.instance)
		if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
			raise ValidationError(u'Студент є старостою іншої групи', code='invalid')

		return self.cleaned_data['student_group']

# custom administrate
class StudentAdmin(admin.ModelAdmin):
	actions = ['copy_students']
	list_display = ['id', 'last_name', 'first_name', 'ticket', 'student_group']
	list_display_links = ['last_name', 'first_name']
	list_editable = ['student_group']
	ordering = ['last_name']
	list_filter = ['student_group']
	list_per_page = 10
	search_fields = ['last_name', 'first_name', 'middle_name', 'ticket', 'notes']
	form = StudentFormAdmin

	def view_on_site(self, obj):
		return reverse('students_edit', kwargs={'sid': obj.id})

	def copy_students(self, request, queryset):
		message = ''
		for student in queryset:
			tmpPk = student.pk
			student.pk = None
			student.save()
			if tmpPk != student.pk and isinstance( student.pk, long ):
				message += student.last_name + ', '
		message = message[:-2]
		self.message_user(request, "%s succussfully copied" % message)
	copy_students.short_description = u"Дублювати обраних студентів"

class GroupFormAdmin(ModelForm):

	def clean_leader(self):
		"""Check is any leader at the group
		If not, check is he belong to this group"""
		# get leader of the group
		studentsOurGroup = Student.objects.filter(student_group=self.instance)
		leaderOurGroup = self.cleaned_data['leader']
		if leaderOurGroup is not None:
			if leaderOurGroup in studentsOurGroup:
				return leaderOurGroup
			else:
				raise ValidationError((u'Студент %(stud)s не може бути лідером групи %(group)s, \
									 бо не належить до неї!'), code='invalid',
									 					  params={'stud': leaderOurGroup,
									 					  		  'group': self.instance},
				)
		return leaderOurGroup

class GroupAdmin(admin.ModelAdmin):
	list_display = ['id', 'title', 'leader']
	list_filter = ['title']
	search_fields = ['leader__last_name']
	form = GroupFormAdmin
		

# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Visiting)
admin.site.register(Exam)
admin.site.register(Result_exam)
admin.site.register(MonthJournal)
