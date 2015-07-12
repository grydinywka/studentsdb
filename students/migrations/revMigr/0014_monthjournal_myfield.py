# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0013_monthjournal2'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthjournal',
            name='myField',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
