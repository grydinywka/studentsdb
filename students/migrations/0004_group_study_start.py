# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20150410_0656'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='study_start',
            field=models.DateField(null=True, verbose_name='\u041f\u043e\u0447\u0430\u0442\u043e\u043a \u043d\u0430\u0432\u0447\u0430\u043d\u043d\u044f'),
            preserve_default=True,
        ),
    ]
