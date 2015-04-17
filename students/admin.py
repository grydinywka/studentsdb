from django.contrib import admin
from .models.Student import Student
from .models.Group import Group
from .models.Visiting import Visiting

# Register your models here.
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Visiting)
