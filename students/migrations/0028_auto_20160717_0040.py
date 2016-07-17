# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import students.models.Result_exam


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0027_auto_20160710_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result_exam',
            name='valuetion',
            field=models.DecimalField(verbose_name='Valuetion', max_digits=2, decimal_places=0, validators=[students.models.Result_exam.validate_value]),
        ),
    ]
