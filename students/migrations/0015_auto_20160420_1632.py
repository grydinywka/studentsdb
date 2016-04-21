# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import students.models.Result_exam


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0014_auto_20160420_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logentry',
            name='message',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='module',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='result_exam',
            name='valuetion',
            field=models.DecimalField(verbose_name='\u041e\u0446\u0456\u043d\u043a\u0430', max_digits=2, decimal_places=0, validators=[students.models.Result_exam.validate_value]),
        ),
    ]
