# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('download', '0008_auto_20150507_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='download',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
