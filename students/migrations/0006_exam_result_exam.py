# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import students.models.Result_exam


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20150416_0756'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256, verbose_name='\u041d\u0430\u0437\u0432\u0430')),
                ('exam_date', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0456 \u0447\u0430\u0441 \u0456\u0441\u043f\u0438\u0442\u0443')),
                ('presenter', models.CharField(max_length=256, verbose_name='\u0415\u043a\u0437\u0430\u043c\u0435\u043d\u0430\u0442\u043e\u0440')),
                ('notes', models.TextField(verbose_name='\u0414\u043e\u0434\u0430\u0442\u043a\u043e\u0432\u0456 \u043d\u043e\u0442\u0430\u0442\u043a\u0438', blank=True)),
                ('exam_group', models.ManyToManyField(related_name='exams', null=True, verbose_name='\u0413\u0440\u0443\u043f\u0430 \u0434\u043b\u044f \u0456\u0441\u043f\u0438\u0442\u0443', to='students.Group', blank=True)),
            ],
            options={
                'verbose_name': '\u0406\u0441\u043f\u0438\u0442',
                'verbose_name_plural': '\u0406\u0441\u043f\u0438\u0442\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Result_exam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valuetion', models.DecimalField(verbose_name='\u041e\u0446\u0456\u043d\u043a\u0430', max_digits=2, decimal_places=0, validators=[students.models.Result_exam.validate_value])),
                ('notes', models.TextField(verbose_name='\u0414\u043e\u0434\u0430\u0442\u043a\u043e\u0432\u0456 \u043d\u043e\u0442\u0430\u0442\u043a\u0438', blank=True)),
                ('exams', models.ManyToManyField(to='students.Exam', null=True, verbose_name='\u0406\u0441\u043f\u0438\u0442')),
                ('students', models.ManyToManyField(to='students.Student', null=True, verbose_name='\u0421\u0442\u0443\u0434\u0435\u043d\u0442')),
            ],
            options={
                'verbose_name': '\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442',
                'verbose_name_plural': '\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0438',
            },
            bases=(models.Model,),
        ),
    ]
