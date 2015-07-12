# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0014_monthjournal_myfield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monthjournal2',
            name='monthjournal_ptr',
        ),
        migrations.DeleteModel(
            name='MonthJournal2',
        ),
        migrations.RemoveField(
            model_name='monthjournal',
            name='myField',
        ),
    ]
