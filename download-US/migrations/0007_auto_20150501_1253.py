# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import os
from django.conf import settings
from django.db import models, migrations


def downloads_to_product_models(apps, schema_editor):
  Download = apps.get_model('download', 'Download')
  ProductModel = apps.get_model('products', 'Product')

  fixture_path = os.path.join(settings.PROJECT_PATH, 'download', 'fixtures', 'downloads_product_group_to_model.json')

  with open(fixture_path, 'r') as f:
    download_data = json.load(f)
    for download in download_data['downloads']:
      # get download
      try:
        dl = Download.objects.get(file_path=download['file_path'])
      except (Download.DoesNotExist, Download.MultipleObjectsReturned):
        continue


      # empty current product models
      dl.products.clear()

      # assign each product model to download
      for product_model_slug in download['product_model_slugs']:
        try:
          product = ProductModel.objects.get(slug=product_model_slug)
        except (ProductModel.DoesNotExist, ProductModel.MultipleObjectsReturned):
          continue
        dl.products.add(product)

      # clear product groups
      dl.product_groups.clear()
      # save
      dl.save()


def downloads_to_product_models_reverse(apps, schema_editor):
  pass


class Migration(migrations.Migration):

    dependencies = [
        ('download', '0006_auto_20150427_1359'),
    ]

    operations = [
      migrations.RunPython(downloads_to_product_models, reverse_code=downloads_to_product_models_reverse)
    ]
