# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ubntcom.utils.storage
import ubntcom.download.models
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(max_length=200)),
                ('date_to_publish', models.DateField(null=True, blank=True)),
                ('is_legacy', models.BooleanField(default=False, help_text='Is this document for a legacy product? Legacy downloads appear<br />on the download page and not on the product detail page.')),
                ('document_path', models.CharField(help_text='ex: datasheets/airfiber/airFiber_DS.pdf', max_length=300)),
                ('thumbnail', models.ImageField(storage=ubntcom.utils.storage.OverwriteStorage(), null=True, upload_to=ubntcom.download.models.thumbnail_path, blank=True)),
                ('thumbnail_retina', models.ImageField(storage=ubntcom.utils.storage.OverwriteStorage(), null=True, upload_to=ubntcom.download.models.thumbnail_path, blank=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('category__order', 'name'),
                'verbose_name_plural': 'Downloads',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DownloadCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('order', models.IntegerField(unique=True, null=True)),
            ],
            options={
                'ordering': ('order',),
                'verbose_name_plural': 'Download Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DownloadSubscriber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75, verbose_name=b'Email Address')),
                ('product', models.CharField(default=b'airmax', max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='download',
            name='category',
            field=models.ForeignKey(to='download.DownloadCategory'),
            preserve_default=True,
        ),
    ]
