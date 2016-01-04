# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('firmware', '0003_auto_20150407_0916'),
        ('products', '0003_auto_20150331_0930'),
        ('download', '0003_auto_20150407_0928'),
    ]

    operations = [
        migrations.RenameField(
            model_name='download',
            old_name='document_path',
            new_name='file_path',
        ),
        migrations.RemoveField(
            model_name='download',
            name='date_to_publish',
        ),
        migrations.RenameField(
            model_name='download',
            old_name='product_group',
            new_name='product_groups',
        ),
        migrations.AddField(
            model_name='download',
            name='architecture',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='download',
            name='build',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='download',
            name='changelog',
            field=models.CharField(help_text='The changelog path from /var/www/downloads/ on dl.ubnt.com. Example: firmwares/XW-fw/v5.5.9/changelog.txt', max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='download',
            name='date_published',
            field=models.DateField(default=datetime.date.today, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='download',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='download',
            name='download_count',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='download',
            name='mib',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='download',
            name='product_family',
            field=models.ForeignKey(blank=True, to='products.ProductFamily', null=True),
        ),
        migrations.AddField(
            model_name='download',
            name='products',
            field=sortedm2m.fields.SortedManyToManyField(help_text='Select Product Models supported by this download.', related_name='downloads', to='products.Product', blank=True),
        ),
        migrations.AddField(
            model_name='download',
            name='revision_history',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='download',
            name='sdk',
            field=models.ForeignKey(blank=True, to='firmware.FirmwareSDK', null=True),
        ),
        migrations.AddField(
            model_name='download',
            name='size',
            field=models.CharField(help_text=b'The file size of the download. Example: 60MB', max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='download',
            name='version',
            field=models.CharField(help_text='The version of this download. Example: v5.5.9', max_length=50, blank=True),
        ),
    ]
