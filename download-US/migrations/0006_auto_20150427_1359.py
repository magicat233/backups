# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
from django.template.defaultfilters import slugify


def populate_utilties(apps, schema_editor):
    Download = apps.get_model('download', 'Download')
    DownloadCategory = apps.get_model('download', 'DownloadCategory')

    category, created = DownloadCategory.objects.get_or_create(name='Utilities', slug='utilities')

    # Discovery Tool Java
    dl = Download()
    dl.name = 'Device Discovery Tool (Java - All platforms)'
    dl.slug = slugify(dl.name)
    dl.date_published = '2014-11-19'
    dl.category = category
    dl.file_path = 'discovery/ubnt-discovery-v2.4.1.zip'
    dl.description = ''
    dl.version = 'v2.4.1'
    dl.build = ''
    dl.architecture = ''
    dl.mib = ''
    dl.revision_history = ''
    dl.changelog = '/discovery/Changelog.txt'
    dl.size = '144 KB'
    dl.save()

    # Discovery Tool Mac OS X Bundle
    dl = Download()
    dl.name = 'Device Discovery Tool (Java - Mac OS X Bundle)'
    dl.slug = slugify(dl.name)
    dl.date_published = '2014-11-19'
    dl.category = category
    dl.file_path = 'discovery/Discovery Tool-v2.4.1.app.tar'
    dl.description = ''
    dl.version = 'v2.4.1'
    dl.build = ''
    dl.architecture = ''
    dl.mib = ''
    dl.revision_history = ''
    dl.changelog = '/discovery/Changelog.txt'
    dl.size = '287 KB'
    dl.save()

    # Outdoor Wireless Link Calculator
    dl = Download()
    dl.name = 'Outdoor Wireless Link Calculator'
    dl.slug = slugify(dl.name)
    dl.date_published = None
    dl.category = category
    dl.file_path = 'http://airlink.ubnt.com/'
    dl.description = 'airLink™ requires that you download and install the Google Earth plug-in.'
    dl.version = ''
    dl.build = ''
    dl.architecture = ''
    dl.mib = ''
    dl.revision_history = ''
    dl.changelog = ''
    dl.size = ''
    dl.save()

    # Discovery Tool Chrome Extension
    dl = Download()
    dl.name = 'Ubiquiti Discovery Tool (Chrome Extension)'
    dl.slug = slugify(dl.name)
    dl.date_published = '2015-03-11'
    dl.category = category
    dl.file_path = 'https://chrome.google.com/webstore/detail/ubiquiti-discovery-tool/hmpigflbjeapnknladcfphgkemopofig?hl=en'
    dl.description = ''
    dl.version = ''
    dl.build = ''
    dl.architecture = ''
    dl.mib = ''
    dl.revision_history = ''
    dl.changelog = ''
    dl.size = ''
    dl.save()

    

def populate_utilties_reverse(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('download', '0005_auto_20150421_1808'),
    ]

    operations = [
        migrations.RunPython(populate_utilties, reverse_code=populate_utilties_reverse)
    ]
