# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Download.thumbnail'
        db.add_column(u'download_download', 'thumbnail',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Download.thumbnail_retina'
        db.add_column(u'download_download', 'thumbnail_retina',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Download.thumbnail'
        db.delete_column(u'download_download', 'thumbnail')

        # Deleting field 'Download.thumbnail_retina'
        db.delete_column(u'download_download', 'thumbnail_retina')


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
            'document_path': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'product_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.ProductGroup']", 'null': 'True', 'blank': 'True'}),
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
        u'download.downloadsubscriber': {
            'Meta': {'object_name': 'DownloadSubscriber'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.CharField', [], {'default': "'airmax'", 'max_length': '100'})
        },
        u'products.productfamily': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ProductFamily'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.ProductFamilyCategory']"}),
            'community_blog_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'featured_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'logo_retina': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'products.productfamilycategory': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ProductFamilyCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'products.productfeature': {
            'Meta': {'object_name': 'ProductFeature'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'image_alt_text': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image_retina': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'products.productgroup': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ProductGroup'},
            'accessories': ('sortedm2m.fields.SortedManyToManyField', [], {'blank': 'True', 'related_name': "'accessories_rel_+'", 'null': 'True', 'to': u"orm['products.ProductGroup']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_to_publish': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.ProductFamily']"}),
            'feature_theme': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'feature_theme'", 'null': 'True', 'to': u"orm['products.ProductTheme']"}),
            'features': ('sortedm2m.fields.SortedManyToManyField', [], {'blank': 'True', 'related_name': "'features+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['products.ProductFeature']"}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'hero_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'hero_image_background': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'hero_image_background_retina': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'hero_image_retina': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'icon_font_css_class': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'legacy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'legacy_product_redirect': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['products.ProductGroup']"}),
            'medium_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'medium_image_retina': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'related_products': ('sortedm2m.fields.SortedManyToManyField', [], {'blank': 'True', 'related_name': "'related_products_rel_+'", 'null': 'True', 'to': u"orm['products.ProductGroup']"}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'small_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'small_image_retina': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.ProductTheme']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'products.producttheme': {
            'Meta': {'object_name': 'ProductTheme'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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