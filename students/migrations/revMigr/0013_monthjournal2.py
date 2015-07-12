# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0012_auto_20150709_0438'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthJournal2',
            fields=[
                ('monthjournal_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='students.MonthJournal')),
            ],
            options={
                'abstract': False,
            },
            bases=('students.monthjournal',),
        ),
    ]
