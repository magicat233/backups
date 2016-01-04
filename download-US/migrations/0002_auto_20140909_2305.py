# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('taggit', '0001_initial'),
        ('download', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='download',
            name='product_group',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name=b'product_group', to='products.ProductGroup', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='download',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
    ]
