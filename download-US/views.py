import os
import json
import datetime
import mailchimp
from django.conf import settings
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.cache import cache
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView, View, RedirectView
from django.db.models import Q, F
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from haystack.query import SearchQuerySet, SQ
from waffle.decorators import waffle_flag
from ubntcom.firmware.models import FirmwareSDK
from ubntcom.products.models import ProductFamily, Product, ProductGroup
from ubntcom.search.utils import AutoCompleteSearch
from .models import Download

SEO_FRAGMENT_SLUG = '_escaped_fragment_'

PRODUCT_FAMILY_DEFAULT_SLUG = 'airmax-ac'

# Top level (family) mapping for airmax-ac, airmax-m, airmax-legacy
PRODUCT_FAMILY_SEGMENT_MAP = {
    'airmax-ac': {'product_family_slug': 'airmax', 'is_ac_product': True, 'legacy': False},
    'airmax-m': {'product_family_slug': 'airmax', 'is_ac_product': False, 'legacy': False},
    'airmax-legacy': {'product_family_slug': 'airmax', 'legacy': True},
}

# Group level mapping to group query args for group lookup
PRODUCT_GROUP_SEGMENT_MAP = {
    'unifi-legacy': {'family__slug': 'unifi', 'legacy': True},
    'airgrid-m-legacy-models': {'slug': 'airgridm', 'legacy_products': True}
}

# Mapping of allowable family slugs to their actual slug
ALLOWED_FAMILY_SLUGS_MAP = {
    'unifivideo': 'unifi-video',
    'airvision': 'unifi-video',
    'airmax': 'airmax-ac',
}

class DownloadView(TemplateView):
    template_name = 'support/downloads_accordian.html'
    search = False

    # Do not use the middleware cache on this
    # view. Caching should be implemented
    # directly on the queries instead.
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(DownloadView, self).dispatch(*args, **kwargs)

    def is_ajax_request(self):
        """
        Shortcut to allow debugging
        JSON responses.
        """
        return self.request.is_ajax() or ('json' in self.request.GET and settings.DEBUG)

    def get_platform_tree(self):
        tree = []
        platform_slugs = ['airmax', 'airfiber', 'edgemax', 'mfi', 'sunmax', 'unifi', 'unifi-video', 'unifi-switching-routing', 'unifi-voip', 'accessories']

        for platform_slug in platform_slugs:
            tree.append(self.get_productgroups_by_family(platform_slug))

        return tree

    # !! TODO: cache and optimize when ready
    def get_productgroups_by_family(self, product_family_slug):
        product_object = {}
        
        # get product family/platform
        product_family = ProductFamily.objects.get(slug=product_family_slug)
        product_object['product_family'] = product_family

        # airmax is unique and has ac and m series product groups
        if product_family_slug == 'airmax':            
            # get airmax ac products
            products_ac = product_family.sorted_products.filter(is_ac_product=True).public_noSort()
            if products_ac.exists():
                product_object['products_ac'] = products_ac    

            # get airmax m series products
            products = product_family.sorted_products.filter(is_ac_product=False).public_noSort()
            if products.exists():
                product_object['products_m'] = products

        else:
            # get product family's products
            # exclude airfiber, unifi voip overview microsites
            products = self.get_productgroups(False, product_family).exclude(slug='airfiber').exclude(family__slug='unifi-voip', slug='overview').public_noSort()
            if products.exists():
                product_object['products'] = products.order_by('slug')


        # airvision are legacy products for unifi-video
        if product_family_slug == 'unifi-video':
            legacy_products = self.get_productgroups(True, ProductFamily.objects.get(slug='airvision')).public_noSort()
            if products.exists():
                product_object['legacy_products'] = legacy_products.order_by('slug')
        else:
            # get product family's legacy products
            legacy_products = self.get_productgroups(True, product_family).public_noSort()
            if legacy_products.exists():
                product_object['legacy_products'] = legacy_products.order_by('slug')

        return product_object

    def get_productgroups(self, is_legacy, product_family):
        return ProductGroup.objects.filter(legacy=is_legacy, family=product_family)

    def get_product_family(self, product_family_slug):
        try:
            return ProductFamily.objects.get(slug=product_family_slug)
        except (ProductFamily.DoesNotExist, ProductFamily.MultipleObjectsReturned):
            return None

    def get_product_group(self, product_group_slug=None, group_query_args=None):
        if group_query_args:
            query_args = group_query_args
        elif product_group_slug:
            query_args = {'slug': product_group_slug}
        else:
            return None
        
        try:
            return ProductGroup.objects.public_noSort().get(**query_args)
        except (ProductGroup.DoesNotExist, ProductGroup.MultipleObjectsReturned):
            return None

    def get_product(self, product_slug):
        try:
            return Product.objects.public_noSort().get(slug=product_slug)
        except (Product.DoesNotExist, Product.MultipleObjectsReturned):
            return None

    def get_downloads_cache_key(self, product_family_slug, product_group_slug, 
            product_slug, is_ac_product, legacy):
        key_parts = ['download', 'get_downloads']

        if product_family_slug:
            key_parts.append(product_family_slug)

        if is_ac_product is not None:
            key_parts.append('is_ac_product:1' if is_ac_product else 'is_ac_product:0')

        if legacy is not None:
            key_parts.append('legacy:1' if is_ac_product else 'legacy:0')

        if product_group_slug:
            key_parts.append('productgroup:'+product_group_slug)

        if product_slug:
            key_parts.append('product:'+product_slug)

        return ':'.join(key_parts)

    def get_downloads(self, product_family_slug, product_group_slug, 
            product_slug, is_ac_product=None, legacy=None, group_query_args=None,
            legacy_products=None):
        """
        Find the downloads associated with a Family, Group, or Product
        in that order of precedence.
        """
        cache_key = self.get_downloads_cache_key(product_family_slug, product_group_slug, 
            product_slug, is_ac_product, legacy)

        cached = cache.get(cache_key)
        if cached:
            return cached

        # This is an ugly fix but `unifi-video-legacy` is 
        # on the group level but needs to be looked up 
        # by the `airvision` product family
        if product_group_slug == 'unifi-video-legacy':
            product_family_slug = 'airvision'
            legacy = True

        # utilities aren't tied to a specific family, group, or product
        if product_family_slug == 'utilities':
            downloads = Download.objects.filter(category__slug='utilities').public_noSort()

        # Look up downloads by product family
        elif product_family_slug:

            # Look up the product family
            product_family = self.get_product_family(product_family_slug)
            if not product_family:
                return None

            groups = product_family.productgroup_set.public_noSort()
            
            if is_ac_product is not None:
                groups = groups.filter(is_ac_product=is_ac_product)

            if legacy is not None:
                groups = groups.filter(legacy=legacy)

            group_ids = list(groups.values_list('id', flat=True))
            downloads = Download.objects.filter(
                Q(product_groups__id__in=group_ids) |
                Q(products__group__id__in=group_ids) |
                Q(product_family=product_family)
            )

        # Look up downloads by product group
        elif product_group_slug:
            
            # Look up group with arguments if they exist
            if group_query_args:
                product_group = self.get_product_group(group_query_args=group_query_args)
            else:
                # Look up the product group directly
                product_group = self.get_product_group(product_group_slug=product_group_slug)
            if not product_group:
                return None

            downloads = Download.objects.filter(
                Q(product_groups=product_group) |
                Q(products__group=product_group) |
                Q(product_family=product_group.family)
            )

            if legacy_products is not None:
                products = Product.objects.filter(group=product_group, legacy=legacy_products).values_list('id', flat=True)
                downloads = downloads.filter(products__id__in=products)

        # Look up downloads by product
        elif product_slug:
            
            # Look up the product
            product = self.get_product(product_slug)
            if not product:
                return None

            product_groups = list(product.group.public_noSort().values_list('id', flat=True))
            families = ProductFamily.objects.filter(
                productgroup__id__in=product_groups).values_list('id', flat=True)

            downloads = Download.objects.filter(
                Q(products=product) |
                Q(product_groups__id__in=product_groups) |
                Q(product_family__id__in=families)
            )

        # Use a custom select to add rank using 
        # DENSE_RANK over the download_count
        downloads = downloads.extra(select={
            'rank': 'DENSE_RANK() OVER(ORDER BY download_count DESC)'
        }).public_noSort().distinct().order_by('rank')

        cache.set(cache_key, downloads)
        return downloads

    def get_products_by_group(self, product_group_slug, is_ac_product=None,
        legacy=None, group_query_args=None, legacy_products=None):
        
        # This is an ugly fix but `unifi-video-legacy` is 
        # on the group level but needs to be looked up 
        # by the `airvision` product family
        if product_group_slug == 'unifi-video-legacy':
            products = Product.objects.public_noSort().filter(group__family__slug='airvision', group__legacy=True)
        # Look up with group query
        elif group_query_args:
            group = ProductGroup.objects.public_noSort().filter(**group_query_args)
            products = Product.objects.public_noSort().filter(group=group)
        else:
            products = Product.objects.public_noSort().filter(group__slug=product_group_slug)

        if is_ac_product is not None:
            products = products.filter(group__is_ac_product=is_ac_product)

        if legacy is not None:
            products = products.filter(group__legacy=legacy)

        if legacy_products is not None:
            products = products.filter(legacy=legacy_products)

        return products

    def get_products_by_download(self, download):
        cache_key = 'download:get_products_by_download:{}'.format(download.pk)

        cached = cache.get(cache_key)
        if cached:
            return cached

        # get products that have been directly assigned
        product_ids = list(download.products.public_noSort().values_list('id', flat=True))

        # get products from assigned groups
        group_ids = download.product_groups.public_noSort().values_list('id', flat=True)
        product_ids = product_ids + list(Product.objects.public_noSort().filter(
            group__id__in=group_ids).values_list('id', flat=True))

        # get products from assigned family
        if download.product_family:
            group_ids_from_family = download.product_family.sorted_products. \
                public_noSort().values_list('id', flat=True)
            product_ids = product_ids + list(Product.objects.public_noSort().filter(
                group__id__in=group_ids_from_family).values_list('id', flat=True))


        products = Product.objects.public_noSort().filter(id__in=product_ids)
        cache.set(cache_key, products)

        return products

    def get_download(self):
        download_id = None

        firmware_id = self.request.GET.get('firmware')
        software_id = self.request.GET.get('software')
        gpl_id = self.request.GET.get('gpl')

        if gpl_id:
            try:
                download = FirmwareSDK.objects.get(id=gpl_id)
            except FirmwareSDK.DoesNotExist:
                return ''
            return '/downloads/{}'.format(download.sdk_file_path)

        download_id = firmware_id or software_id
        if download_id:
            try:
                download = Download.objects.get(id=download_id)
            except Download.DoesNotExist:
                return ''

            # Increment the download_count
            # on the download model for this 
            # firmware or software download.
            download.increment_download_count()

            return download.get_absolute_download_path()
        return ''

    def get_downloads_to_serialize(self, downloads):
        included_downloads = []
        downloads_to_serialize = []
        if downloads:
            for download in downloads:
                if download.id in included_downloads:
                    continue

                download_products = self.get_products_by_download(download)
                download_products_repr = '|'.join(download_products.values_list('name', flat=True))

                download_dict = download.to_dict()
                download_dict['products'] = download_products_repr
                download_dict['rank'] = getattr(download, 'rank', '')

                included_downloads.append(download.id)
                downloads_to_serialize.append(download_dict) 

        return downloads_to_serialize

    def get_search_results_context(self, **kwargs):
        context = super(DownloadView, self).get_context_data(**kwargs)
        context['products'] = []

        query = self.request.GET.get('q')

        if query:
            result_models = []
            base_search_qs = SearchQuerySet().models(Download)
            clean_query = base_search_qs.query.clean(query).strip()

            # Enable partial string searches by using *
            if ' ' in clean_query:
                search_query = clean_query.replace(' ', '* ')
            else:
                search_query = '{}*'.format(clean_query)

            results = base_search_qs.raw_search('text:{}'.format(search_query))

            for result in results:
                # Skip the result if the download object does not exist in the DB
                if not result.object:
                    continue

                result_models.append(result.object)

            context['downloads'] = self.get_downloads_to_serialize(result_models)
        return context

    def get_downloads_context(self, **kwargs):
        context = super(DownloadView, self).get_context_data(**kwargs)

        context['downloads'] = []
        context['products'] = []

        products = None
        is_ac_product = None
        legacy = None
        legacy_products = None
        group_query_args = None
        product_group_slug = self.request.GET.get('group')
        product_slug = self.request.GET.get('product')

        # Product family slug is passed in as `platform`
        # family slug deeplinked (ie: /download/airfiber/)
        product_family_slug = self.kwargs.get('platform') or self.request.GET.get(SEO_FRAGMENT_SLUG)

        # ?platform GET variable takes precedence over
        # the deeplinked family slug
        product_family_slug = self.request.GET.get('platform', product_family_slug)

        # If we are not filtering against anything use 
        # the default family slug
        if not product_family_slug and not product_group_slug and not product_slug:
            product_family_slug = PRODUCT_FAMILY_DEFAULT_SLUG

        # Handle custom segmented product families
        if product_family_slug in PRODUCT_FAMILY_SEGMENT_MAP:
            segment = PRODUCT_FAMILY_SEGMENT_MAP[product_family_slug]
            is_ac_product = segment.get('is_ac_product')
            legacy = segment.get('legacy')
            product_family_slug = segment['product_family_slug']
        # Handle allowable slugs (unifivideo -> unifi-video)
        elif product_family_slug in ALLOWED_FAMILY_SLUGS_MAP:
            product_family_slug = ALLOWED_FAMILY_SLUGS_MAP[product_family_slug]

        # Handle custom segmented  product groups
        if product_group_slug in PRODUCT_GROUP_SEGMENT_MAP:
            group_query_args = PRODUCT_GROUP_SEGMENT_MAP[product_group_slug]
            if 'legacy_products' in group_query_args:
                legacy_products = group_query_args.pop('legacy_products')

        downloads = self.get_downloads(product_family_slug, product_group_slug, 
            product_slug, is_ac_product=is_ac_product, legacy=legacy,
            group_query_args=group_query_args, legacy_products=legacy_products)

        context['downloads'] = self.get_downloads_to_serialize(downloads)

        if product_group_slug:
            products = self.get_products_by_group(product_group_slug, is_ac_product, legacy, 
                group_query_args, legacy_products)
            if products:
                context['products'] = list(products.values('slug', 'name', 'legacy'))

        return context

    def get_context_data(self, **kwargs):
        context = super(DownloadView, self).get_context_data(**kwargs)

        # Only get downloads (or downloads search results) if this is an ajax request
        # or has _escaped_fragment_ GET param for SEO results.
        if self.is_ajax_request() or self.request.GET.get(SEO_FRAGMENT_SLUG):  
            if self.search and 'q' in self.request.GET.keys():
                context.update(self.get_search_results_context(**kwargs))
            else:
                context.update(self.get_downloads_context(**kwargs))

        product_family_slug = self.kwargs.get('platform')
        # Convert to actual slug if this
        # is an allowable family slug
        if product_family_slug in ALLOWED_FAMILY_SLUGS_MAP:
            product_family_slug = ALLOWED_FAMILY_SLUGS_MAP[product_family_slug]

        # clean url deeplink support (/airfiber/[airfiber24]/[af24])
        context.update({'deeplink_platform_slug': product_family_slug})
        context.update({'deeplink_product_group_slug': self.kwargs.get('product_group')})
        context.update({'deeplink_product_model_slug': self.kwargs.get('product_model')})
        context.update({'deeplink_product_item_slug': self.kwargs.get('product_item')})

        return context

    def post(self, request, *args, **kwargs):
        ret = {}
        #update notifcation form
        if self.is_ajax_request() and 'email' in request.POST:
            email = request.POST['email']
            msg = _('Thank you for signing up for future updates.') 

            mailchimp_api_key = getattr(settings, 'MAILCHIMP_API_KEY', '')
            list_id = getattr(settings, 'MAILCHIMP_AIRMAX_UPDATES_ID', '')

            try:
                mailchimp_api = mailchimp.Mailchimp(mailchimp_api_key)
                r = mailchimp_api.lists.subscribe(list_id, {
                        'email': email
                    }
                )
            except mailchimp.ListAlreadySubscribedError:
                #msg = _('You have already signed up for these updates.')
                pass
            except mailchimp.Error, e:
                #print 'An error occurred: %s - %s' % (e.__class__, e)
                pass
            #ret['msg'] = msg

        return HttpResponse(json.dumps(ret), content_type='application/json')

    def render_to_response(self, context, **response_kwargs):

        # add ?json to /download to view json for testing/debugging.
        if self.is_ajax_request():
            data = {}
            if 'firmware' in self.request.GET or \
               'software' in self.request.GET or \
               'gpl' in self.request.GET:
                
                # if user agreed to EULA set it in the session
                if 'eula' in self.request.GET:
                    self.request.session['eula_agree'] = True

                # if eula has never been accepted
                if not self.request.session.get('eula_agree', False):
                    data['eula'] = False

                # otherwise send download
                else:
                    data['download_url'] = self.get_download()
                    data['eula'] = True
            elif self.search:
                data = {
                    'downloads': context['downloads']
                }
            else:
                data = {
                    'downloads': context['downloads'],
                    'products': context['products'],
                }

            return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')

        # If we have escaped fragment this is a template fragment for SEO.
        if self.request.GET.get(SEO_FRAGMENT_SLUG):
            context['seo_fragment_page'] = True
            context['platform_slug'] = self.request.GET[SEO_FRAGMENT_SLUG]

        # Get the product_tree for the left-hand navigation
        # This is only required when doing backend template
        # rendering. Placing it here avoids it being called
        # during ajax requests.
        context['platform_tree'] = self.get_platform_tree()

        return super(DownloadView, self).render_to_response(context, **response_kwargs)


class DownloadCountView(View):
    """
    AJAX post handler to increment
    download_count on a download.
    Expects `download_id` POST parameter.
    `X-CSRFToken` header required to 
    prevent abuse.
    """
    http_method_names = ['post']

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(DownloadCountView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        download_id = self.request.POST.get('download_id')
        if self.request.is_ajax() and (download_id and download_id.isdigit()):
            Download.objects.filter(id=download_id).update(download_count_tracked=F('download_count_tracked') + 1)
        return HttpResponse()


@waffle_flag('search_autocomplete')
def search_autocomplete(request):
    """
    Auto complete view for download search
    Returns JSON list
    """

    ret = []

    if 'q' in request.GET.keys():
        query = request.GET['q']
        ret = AutoCompleteSearch(models=Download).search(query)

    return HttpResponse(json.dumps(ret), content_type='application/json')


class DownloadRedirectView(RedirectView):

    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        """
        Use the https download URL if the incoming connection was also 
        under https, otherwise use http.
        """
        if self.request.is_secure():
            base_url = settings.DOWNLOAD_URL_SECURE
        else:
            base_url = settings.DOWNLOAD_URL

        return os.path.join(base_url, '%(slug)s'.strip('/')) % kwargs
