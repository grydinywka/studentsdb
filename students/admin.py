from django.contrib import admin
from .models.Student import Student
from .models.Group import Group
from .models.Visiting import Visiting
from .models.Exam import Exam
from .models.Result_exam import Result_exam

# Register your models here.
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Visiting)
admin.site.register(Exam)
admin.site.register(Result_exam)
