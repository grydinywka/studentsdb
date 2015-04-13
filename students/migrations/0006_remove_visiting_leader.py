# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_visiting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visiting',
            name='leader',
        ),
    ]
