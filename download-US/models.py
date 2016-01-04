import os
import datetime
from django.db import models
from django.db.models import F
from django.utils.translation import ugettext as _
from sortedm2m.fields import SortedManyToManyField
from taggit.managers import TaggableManager
from ubntcom.utils.storage import OverwriteStorage
from ubntcom.products.models import ProductFamily, ProductGroup, Product
from ubntcom.firmware.models import FirmwareSDK


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
class DownloadQuerySet(models.QuerySet):
    # public downloads
    def public_noSort(self):
        return self.exclude(date_published__gt=datetime.date.today())

    # only public documentation
    def only_documentation(self):
        return self.exclude(category__slug='firmware').exclude(category__slug='software').public_noSort().select_related('category')

    # only public firmware
    def only_firmware(self):
        return self.filter(category__slug='firmware').public_noSort().select_related('category')

    # only public software
    def only_software(self):
        return self.filter(category__slug='software').public_noSort().select_related('category')


class Download(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200)
    featured = models.BooleanField(default=False)
    date_published = models.DateField(blank=True, null=True, default=datetime.date.today)
    is_legacy = models.BooleanField(default=False, help_text=_('Is this document for a legacy product? Legacy downloads appear'\
            '<br />on the download page and not on the product detail page.'))
    category = models.ForeignKey(DownloadCategory)
    product_family = models.ForeignKey(ProductFamily, blank=True, null=True, related_name='downloads')
    product_groups = SortedManyToManyField(ProductGroup, blank=True, related_name='downloads')
    products = SortedManyToManyField(Product, blank=True, related_name='downloads', help_text=_('Select Product Models supported by this download.'))
    file_path = models.CharField(max_length=300, help_text=_('ex: datasheets/airfiber/airFiber_DS.pdf'))
    thumbnail = models.ImageField(upload_to=thumbnail_path, blank=True, null=True, storage=OverwriteStorage())
    thumbnail_retina = models.ImageField(upload_to=thumbnail_path, blank=True, null=True, storage=OverwriteStorage())
    description = models.TextField(blank=True)
    version = models.CharField(max_length=50, blank=True, help_text=_('The version of this download. Example: v5.5.9'))
    build = models.CharField(max_length=50, blank=True)
    architecture = models.CharField(max_length=50, blank=True)
    mib = models.CharField(max_length=200, blank=True)
    sdk = models.ForeignKey(FirmwareSDK, blank=True, null=True)
    revision_history = models.TextField(blank=True)
    changelog = models.CharField(blank=True, max_length=200, help_text=_('The changelog path from /var/www/downloads/ on dl.ubnt.com. '\
        'Example: firmwares/XW-fw/v5.5.9/changelog.txt'))
    size = models.CharField(max_length=50, blank=True, null=True, help_text=('The file size of the download. Example: 60MB'))
    download_count = models.PositiveIntegerField(editable=False, default=0, help_text=_('The download count total that determines rank'))
    download_count_tracked = models.PositiveIntegerField(editable=False, default=0, help_text=_('The currently tracked download count'))
    tags = TaggableManager(blank=True)
    last_modified = models.DateTimeField(auto_now=True)

    # manager
    objects = DownloadQuerySet.as_manager()

    def get_product_groups_for_admin(self):
        return '<br />'.join([p.name for p in self.product_groups.all()])
    get_product_groups_for_admin.short_description = 'Product Groups'
    get_product_groups_for_admin.allow_tags = True

    def get_product_models_for_admin(self):
        return '<br />'.join([p.name for p in self.products.all()])
    get_product_models_for_admin.short_description = 'Product Models'
    get_product_models_for_admin.allow_tags = True

    @property
    def filename(self):
        return ''.join(self.file_path.split('/')[-1:])

    def to_dict(self):
        ret = {}
        ret['id'] = self.id
        ret['name'] = self.name
        ret['slug'] = self.slug
        ret['date_published'] = self.date_published.strftime('%Y-%m-%d') if self.date_published else None
        ret['file_path'] = self.get_absolute_download_path()
        ret['category__name'] = self.category.name
        ret['category__slug'] = self.category.slug
        ret['thumbnail'] = self.thumbnail.url if self.thumbnail else None
        ret['thumbnail_retina'] = self.thumbnail_retina.url if self.thumbnail_retina else None
        ret['description'] = self.description
        ret['version'] = self.version
        ret['build'] = self.build
        ret['architecture'] = self.architecture
        ret['mib'] = self.mib
        ret['sdk__id'] = self.sdk_id
        ret['revision_history'] = self.revision_history
        ret['changelog'] = self.changelog
        ret['size'] = self.size
        ret['featured'] = self.featured
        ret['filename'] = self.filename
        return ret

    def get_absolute_download_path(self):
        if self.file_path.startswith('http'):
            return self.file_path
        return '/downloads/{}'.format(self.file_path)

    def increment_download_count(self):
        self.download_count_tracked = F('download_count_tracked') + 1
        self.save()

    def get_family_deeplink(self):
        """
        Get a family object and deeplink to this download. 
        Used for download search results
        """
        product_group = None
        subsection = 'default'

        if self.product_family:
            family = self.product_family
        elif self.product_groups.all():
            product_group = self.product_groups.all()[0]
            family = product_group.family
        elif self.products.all():
            try:
                product_group = self.products.all()[0].group.all()[0]
                family = product_group.family
            except IndexError:
                return None

        # Handle Airmax segmentation for downloads
        # Airmax is segmented into airmax-ac, airmax-m and airmax-legacy
        # on the downloads page, but not on the products pages.
        if family.slug == 'airmax' and product_group:
            if product_group.is_ac_product:
                family_slug = 'airmax-ac'
            elif product_group.legacy:
                family_slug = 'airmax-legacy'
            else:
                family_slug = 'airmax-m'
        else:
            family_slug = family.slug

        # Airvision is legacy unifi-video
        if family_slug == 'airvision':
            family_slug = 'unifi-video'
            subsection = 'unifi-video-legacy'

        return {'family': family, 'deeplink': '/download/{}/{}/default/{}'.format(family_slug, subsection, self.slug)}

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
