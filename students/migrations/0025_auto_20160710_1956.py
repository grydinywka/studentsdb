# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import students.models.Result_exam


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0024_auto_20160521_1358'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='daycounterrequest',
            options={'verbose_name': 'Daily counter of requests', 'verbose_name_plural': 'Dailies counters of requests'},
        ),
        migrations.AlterModelOptions(
            name='exam',
            options={'verbose_name': 'Exam', 'verbose_name_plural': 'Exams'},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'Group', 'verbose_name_plural': 'Groups'},
        ),
        migrations.AlterModelOptions(
            name='monthjournal',
            options={'verbose_name': 'Month Journal', 'verbose_name_plural': 'Month Journals'},
        ),
        migrations.AlterModelOptions(
            name='result_exam',
            options={'verbose_name': 'Result', 'verbose_name_plural': 'Results'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'Student', 'verbose_name_plural': 'Students'},
        ),
        migrations.AlterModelOptions(
            name='visiting',
            options={'verbose_name': 'Visiting', 'verbose_name_plural': 'All Visiting'},
        ),
        migrations.AlterField(
            model_name='daycounterrequest',
            name='counter',
            field=models.IntegerField(default=0, verbose_name='Counter'),
        ),
        migrations.AlterField(
            model_name='daycounterrequest',
            name='date',
            field=models.DateField(unique=True, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='exam_date',
            field=models.DateTimeField(null=True, verbose_name='Date and time of exam'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='exam_group',
            field=models.ManyToManyField(related_name='exams', verbose_name='Groups for exam', to='students.Group', blank=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='notes',
            field=models.TextField(verbose_name='Notes', blank=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='presenter',
            field=models.CharField(max_length=256, verbose_name='Presenter'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='group',
            name='leader',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='students.Student', verbose_name='Leader'),
        ),
        migrations.AlterField(
            model_name='group',
            name='notes',
            field=models.TextField(verbose_name='Notes', blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='monthjournal',
            name='date',
            field=models.DateField(verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='monthjournal',
            name='student',
            field=models.ForeignKey(unique_for_month=b'date', verbose_name='Student', to='students.Student'),
        ),
        migrations.AlterField(
            model_name='result_exam',
            name='exams',
            field=models.ManyToManyField(to='students.Exam', verbose_name='Exams'),
        ),
        migrations.AlterField(
            model_name='result_exam',
            name='notes',
            field=models.TextField(verbose_name='Notes', blank=True),
        ),
        migrations.AlterField(
            model_name='result_exam',
            name='students',
            field=models.ManyToManyField(to='students.Student', verbose_name='Students'),
        ),
        migrations.AlterField(
            model_name='result_exam',
            name='valuetion',
            field=models.DecimalField(verbose_name='Valuetion', max_digits=2, decimal_places=0, validators=[students.models.Result_exam.validate_value]),
        ),
        migrations.AlterField(
            model_name='student',
            name='birthday',
            field=models.DateField(null=True, verbose_name='Date of birth'),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=256, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=256, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='student',
            name='middle_name',
            field=models.CharField(default=b'', max_length=256, verbose_name='Middle Name', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='notes',
            field=models.TextField(verbose_name='Notes', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.ImageField(upload_to=b'', null=True, verbose_name='Photo', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Group', to='students.Group', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_journal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Journal', blank=True, to='students.Visiting', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='study_start',
            field=models.DateField(null=True, verbose_name='Study begin'),
        ),
        migrations.AlterField(
            model_name='student',
            name='ticket',
            field=models.CharField(max_length=256, verbose_name='Ticket'),
        ),
        migrations.AlterField(
            model_name='visiting',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Title'),
        ),
    ]
