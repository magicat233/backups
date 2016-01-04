# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Download.slug'
        db.alter_column(u'download_download', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=200))

    def backwards(self, orm):

        # Changing field 'Download.slug'
        db.alter_column(u'download_download', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50))

    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'download.download': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Download'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['download.DownloadCategory']"}),
            'document_url': ('django.db.models.fields.URLField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Product']", 'null': 'True', 'blank': 'True'}),
            'product_accessory': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.ProductAccessory']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'thumbnail_retina': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'download.downloadcategory': {
            'Meta': {'ordering': "('name',)", 'object_name': 'DownloadCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'products.product': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Product'},
            'accessories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['products.ProductAccessory']", 'symmetrical': 'False', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.ProductFamily']"}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'hero_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'hero_image_retina': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'legacy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'legacy_product_redirect': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['products.Product']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'related_products': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_products_rel_+'", 'blank': 'True', 'to': u"orm['products.Product']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'small_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'small_image_retina': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'products.productaccessory': {
            'Meta': {'object_name': 'ProductAccessory'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'family': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'+'", 'blank': 'True', 'to': u"orm['products.ProductFamily']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image_retina': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'products.productbullet': {
            'Meta': {'object_name': 'ProductBullet'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'products.productfamily': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ProductFamily'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.ProductFamilyCategory']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'featured_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'featured_headline': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'featured_product': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['products.Product']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'logo_retina': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'product_comparison_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'product_comparison_products': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['products.Product']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'software_section_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'software_section_image_retina': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'software_section_title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'})
        },
        u'products.productfamilycategory': {
            'Meta': {'object_name': 'ProductFamilyCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'products.productsupportlink': {
            'Meta': {'object_name': 'ProductSupportLink'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['download']