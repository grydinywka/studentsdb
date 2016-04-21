# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import students.models.Result_exam


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0013_auto_20150710_0634'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.CharField(max_length=20, verbose_name=b'Level')),
                ('acstime', models.DateTimeField(null=True, verbose_name=b'Date and time event')),
                ('module', models.CharField(max_length=20)),
                ('message', models.CharField(max_length=512)),
            ],
        ),
        migrations.AlterField(
            model_name='exam',
            name='exam_group',
            field=models.ManyToManyField(related_name='exams', verbose_name='\u0413\u0440\u0443\u043f\u0430 \u0434\u043b\u044f \u0456\u0441\u043f\u0438\u0442\u0443', to='students.Group', blank=True),
        ),
        migrations.AlterField(
            model_name='result_exam',
            name='exams',
            field=models.ManyToManyField(to='students.Exam', verbose_name='\u0406\u0441\u043f\u0438\u0442'),
        ),
        migrations.AlterField(
            model_name='result_exam',
            name='students',
            field=models.ManyToManyField(to='students.Student', verbose_name='\u0421\u0442\u0443\u0434\u0435\u043d\u0442'),
        ),
        migrations.AlterField(
            model_name='result_exam',
            name='valuetion',
            field=models.DecimalField(verbose_name='\u041e\u0446\u0456\u043d\u043a\u0430', max_digits=2, decimal_places=0, validators=[students.models.Result_exam.validate_value]),
        ),
    ]
