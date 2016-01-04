# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('download', '0002_auto_20140909_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='downloadsubscriber',
            name='email',
            field=models.EmailField(max_length=254, verbose_name=b'Email Address'),
        ),
    ]
