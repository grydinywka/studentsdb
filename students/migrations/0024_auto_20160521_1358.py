# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import students.models.Result_exam


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0023_auto_20160519_1040'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayCounterRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(unique=True, verbose_name='\u0414\u0430\u0442\u0430')),
                ('counter', models.IntegerField(default=1, verbose_name='\u041b\u0456\u0447\u0438\u043b\u044c\u043d\u0438\u043a')),
            ],
            options={
                'verbose_name': '\u0414\u043e\u0431\u043e\u0432\u0438\u0439 \u043b\u0456\u0447\u0438\u043b\u044c\u043d\u0438\u043a \u0437\u0430\u043f\u0438\u0442\u0456\u0432',
                'verbose_name_plural': '\u0414\u043e\u0431\u043e\u0432\u0456 \u043b\u0456\u0447\u0438\u043b\u044c\u043d\u0438\u043a\u0438 \u0437\u0430\u043f\u0438\u0442\u0456\u0432',
            },
        ),
        migrations.AlterField(
            model_name='result_exam',
            name='valuetion',
            field=models.DecimalField(verbose_name='\u041e\u0446\u0456\u043d\u043a\u0430', max_digits=2, decimal_places=0, validators=[students.models.Result_exam.validate_value]),
        ),
    ]
