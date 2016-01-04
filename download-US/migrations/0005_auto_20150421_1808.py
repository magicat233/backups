# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import os
from django.conf import settings
from django.db import models, migrations
from django.template.defaultfilters import slugify


def migrate_firmware(apps, schema_editor):
    Firmware = apps.get_model('firmware', 'Firmware')
    Download = apps.get_model('download', 'Download')
    DownloadCategory = apps.get_model('download', 'DownloadCategory')

    category, created = DownloadCategory.objects.get_or_create(name='Firmware', slug='firmware')

    for firmware in Firmware.objects.all():
        dl = Download()
        dl.name = ''.join(firmware.firmware_file_path.split('/')[-1:])
        dl.slug = slugify(dl.name)

        # Avoid creating duplicates
        if Download.objects.filter(file_path=firmware.firmware_file_path).exists():
            continue

        if firmware.date_published:
            dl.date_published = firmware.date_published
        else:
            dl.date_published = firmware.last_modified.date()

        dl.category = category
        dl.file_path = firmware.firmware_file_path
        dl.description = firmware.description
        dl.version = firmware.version
        dl.build = firmware.build
        dl.architecture = firmware.architecture
        dl.mib = firmware.mib
        dl.sdk = firmware.sdk
        dl.revision_history = ''
        dl.changelog = firmware.changelog
        dl.size = firmware.size

        dl.save()

        # Add m2m's
        for product in firmware.products.all():
            dl.products.add(product)

            for group in product.group.all():
                dl.product_groups.add(group)


def migrate_software(apps, schema_editor):
    Software = apps.get_model('firmware', 'Software')
    Download = apps.get_model('download', 'Download')
    DownloadCategory = apps.get_model('download', 'DownloadCategory')

    category, created = DownloadCategory.objects.get_or_create(name='Software', slug='software')

    for software in Software.objects.all():
        dl = Download()

        # check for android or iOS software since 
        # they don't follow the same formatting as 
        # the other software objects
        if software.file_path == 'unifi-video/android/':
            dl.name = 'UniFi Video for Android'
        elif software.file_path == 'unifi-video/iOS/':
            dl.name = 'UniFi Video for iOS'
        else:
            dl.name = ''.join(software.file_path.split('/')[-1:])
    
        dl.slug = slugify(dl.name)

        # Avoid creating duplicates
        if Download.objects.filter(file_path=software.file_path, product_family=software.family).exists():
            continue

        if software.date_to_publish:
            dl.date_published = software.date_to_publish
        else:
            dl.date_published = software.last_modified.date()

        dl.category = category
        dl.file_path = software.file_path
        dl.description = software.description
        dl.version = ''
        dl.build = ''
        dl.architecture = ''
        dl.mib = ''
        dl.revision_history = ''
        dl.changelog = ''
        dl.size = software.size
        dl.product_family = software.family

        dl.save()

        for group in dl.product_family.productgroup_set.all():
            dl.product_groups.add(group)


def populate_initial_download_count(apps, schema_editor):
    Download = apps.get_model('download', 'Download')

    fixture_path = os.path.join(settings.PROJECT_PATH, 'download', 
        'fixtures', 'initial_download_count.json')
    
    with open(fixture_path, 'r') as f:
        download_data = json.load(f)
        for download in download_data['downloads']:
            try:
                dl = Download.objects.get(file_path=download['file_path'])
            except (Download.DoesNotExist, Download.MultipleObjectsReturned):
                continue

            dl.download_count = download['download_count']
            dl.download_count_tracked = dl.download_count
            dl.save()


def migrate_firmware_reverse(apps, schema_editor):
    pass


def migrate_software_reverse(apps, schema_editor):
    pass


def populate_initial_download_count_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('download', '0004_auto_20150421_1807'),
    ]

    operations = [
        migrations.RunPython(migrate_firmware, reverse_code=migrate_firmware_reverse),
        migrations.RunPython(migrate_software, reverse_code=migrate_software_reverse),
        migrations.RunPython(populate_initial_download_count, 
            reverse_code=populate_initial_download_count_reverse)
    ]
