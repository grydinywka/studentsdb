# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_remove_visiting_leader'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visiting',
            name='group',
        ),
        migrations.DeleteModel(
            name='Visiting',
        ),
    ]
