# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_group_study_start'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visiting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256, verbose_name='\u041d\u0430\u0437\u0432\u0430')),
            ],
            options={
                'verbose_name': '\u0412\u0456\u0434\u0432\u0456\u0434\u0443\u0432\u0430\u043d\u043d\u044f',
                'verbose_name_plural': '\u0423\u0441\u0456 \u0432\u0456\u0434\u0432\u0456\u0434\u0443\u0432\u0430\u043d\u043d\u044f',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='group',
            name='study_start',
        ),
        migrations.AddField(
            model_name='student',
            name='student_journal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0436\u0443\u0440\u043d\u0430\u043b', blank=True, to='students.Visiting', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student',
            name='study_start',
            field=models.DateField(null=True, verbose_name='\u041f\u043e\u0447\u0430\u0442\u043e\u043a \u043d\u0430\u0432\u0447\u0430\u043d\u043d\u044f'),
            preserve_default=True,
        ),
    ]
