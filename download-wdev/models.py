import os
import datetime
from django.db import models
from ubntcom.products.models import ProductGroup
from taggit.managers import TaggableManager
from django.utils.translation import ugettext as _
from ubntcom.utils.storage import OverwriteStorage
from sortedm2m.fields import SortedManyToManyField
from model_utils.managers import PassThroughManager

def thumbnail_path(instance, filename):
    return os.path.join('images', 'download', instance.category.slug, filename)


class DownloadCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    order = models.IntegerField(unique=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('order',)
        verbose_name_plural = _('Download Categories')

# Querysets used on download
class DownloadQuerySet(models.query.QuerySet):
    # public downloads
    def public_noSort(self):
        return self.exclude(date_to_publish__gt=datetime.date.today())


class Download(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200)
    date_to_publish = models.DateField(blank=True, null=True)
    is_legacy = models.BooleanField(help_text=_('Is this document for a legacy product? Legacy downloads appear<br />on the download page and not on the product detail page.'))
    product_group = SortedManyToManyField(ProductGroup, blank=True, null=True, related_name='product_group')
    category = models.ForeignKey(DownloadCategory)
    document_path = models.CharField(max_length=300, help_text=_('ex: datasheets/airfiber/airFiber_DS.pdf'))
    thumbnail = models.ImageField(upload_to=thumbnail_path, blank=True, null=True, storage=OverwriteStorage())
    thumbnail_retina = models.ImageField(upload_to=thumbnail_path, blank=True, null=True, storage=OverwriteStorage())
    tags = TaggableManager(blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    # manager
    objects = PassThroughManager.for_queryset_class(DownloadQuerySet)()

    def get_product_groups(self):
        return '<br />'.join([p.name for p in self.product_group.all()])
    get_product_groups.short_description = 'Product Groups'
    get_product_groups.allow_tags = True

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('category__order', 'name',)
        verbose_name_plural = 'Downloads'


class DownloadSubscriber(models.Model):
    email = models.EmailField('Email Address')
    product = models.CharField(max_length=100, default='airmax')

    def __unicode__(self):
        return self.email
