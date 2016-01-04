# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('download', '0007_auto_20150501_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='download',
            name='download_count_tracked',
            field=models.PositiveIntegerField(default=0, help_text='The currently tracked download count', editable=False),
        ),
        migrations.AlterField(
            model_name='download',
            name='download_count',
            field=models.PositiveIntegerField(default=0, help_text='The download count total that determines rank', editable=False),
        ),
        migrations.AlterField(
            model_name='download',
            name='product_family',
            field=models.ForeignKey(related_name='downloads', blank=True, to='products.ProductFamily', null=True),
        ),
        migrations.AlterField(
            model_name='download',
            name='product_groups',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='downloads', to='products.ProductGroup', blank=True),
        ),
    ]
