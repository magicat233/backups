import json
import datetime
import json
from django.conf import settings
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.cache import cache
from django.views.decorators.cache import never_cache
from django.views.generic.list import ListView
from django.db.models import Q
from .models import Download
from ubntcom.firmware.models import Firmware, Software, FirmwareSDK
from ubntcom.products.models import ProductFamily, Product, ProductGroup
from django.utils.translation import ugettext as _
import mailchimp


class DownloadView(ListView):
    template_name = 'support/downloads.html'
    model = Download

    # get groups that have firmware or downloads and are under the default platform
    def get_groups(self, platform_id, firmware, download):
        return ProductGroup.objects.filter(Q(id__in=firmware.values('products__group')) | Q(id__in=download.values('product_group')), family__id=platform_id).exclude(date_to_publish__gt=datetime.date.today()).order_by('legacy', 'name')

    def get_group(self, slug):
        return ProductGroup.objects.filter(slug=slug).exclude(date_to_publish__gt=datetime.date.today())

    # get product models that have firmware or download and are under the default group
    def get_models(self, group_id, firmware, download):
        return Product.objects.filter(Q(id__in=firmware.values('products')) | Q(id__in=download.values('product_group')), group__id=group_id).order_by('legacy', 'name')

    # get product model by slug
    def get_model(self, slug):
        return Product.objects.filter(slug=slug)

    # get platforms that have firmware or download
    def get_platforms(self, firmware, download):

        return ProductFamily.objects.filter(Q(id__in=firmware.values('products__group__family')) | Q(id__in=download.values('product_group__family'))).order_by('slug')

    def get_platform(self, slug):
        return ProductFamily.objects.filter(slug=slug)

    def get_firmware(self, product_id, firmware):
        #return firmware.filter(products__id=product_id).exclude(products__date_to_publish__gt=datetime.date.today()).public_noSort()
        return firmware.filter(products__id=product_id).public_noSort()

    def get_downloads(self, product_group, download):
        #return download.filter(product_group__id=product_group.id).exclude(product_group__date_to_publish__gt=datetime.date.today()).public_noSort()
        return download.filter(product_group__id=product_group.id).public_noSort()

    def get_software(self, platform_id, software):
        return software.filter(family__id=platform_id).public_noSort()

    def get_download(self):
        download_id = None
        download_url = '/downloads/'

        if 'firmware' in self.request.GET:
            download_id = self.request.GET['firmware']
            return download_url + Firmware.objects.get(id=download_id).firmware_file_path

        elif 'software' in self.request.GET:
            download_id = self.request.GET['software']
            return download_url + Software.objects.get(id=download_id).file_path

        elif 'gpl' in self.request.GET:
            download_id = self.request.GET['gpl']
            return download_url + FirmwareSDK.objects.get(id=download_id).sdk_file_path

        return ''

    def get_context_data(self, **kwargs):
        context = super(DownloadView, self).get_context_data(**kwargs)

        #print self.kwargs

        firmware = Firmware.objects.all()
        download = Download.objects.all()
        software = Software.objects.all()
        platforms = self.get_platforms(firmware, download)
        platform = None
        group = None
        deeplink_group = None
        groups = None
        products = None
        platform_slug = None
        group_slug = None
        default_platform_slug = 'airmax' # default platform

        context['platforms'] = list(platforms.values('slug', 'name', ))
        context['groups'] = ''
        context['downloads'] = ''
        context['products'] = ''
        context['firmwares'] = ''
        context['software'] = ''

        # check for platform kwarg for deeplinks
        if 'platform' in self.kwargs:
            platform_slug = self.kwargs['platform']

            # allow unifivideo and unifi-video to both work
            if platform_slug == 'unifivideo':
                platform_slug = 'unifi-video'

            # check to make sure platform exists
            platform = self.get_platform(platform_slug)
            if platform:
                # set as default if platform exists
                default_platform_slug = platform_slug
            else:
                platform_slug = None
                platform = None


        # is AJAX?
        # check get parameter
        if 'platform' in self.request.GET:
            platform_slug = self.request.GET['platform']

            # unifi video will you airvision data
            #if platform_slug == 'unifivideo':
            #    platform_slug = 'airvision'

        elif 'group' in self.request.GET:
            group_slug = self.request.GET['group']
            group = self.get_group(group_slug)
            if group:
                # get first productgroup in queryset
                group_item = list(group[:1])
                if group_item:
                    deeplink_group = group_item[0]
                    groups = self.get_groups(deeplink_group.family.id, firmware, download)
        elif 'product' in self.request.GET:
            product_slug = self.request.GET['product']
            products = self.get_model(product_slug)
            
        elif not self.request.GET:
            platform_slug = default_platform_slug

        if platform_slug:
            platform = self.get_platform(platform_slug)


        # groups is set, but not platform_slug
        # get the platform_slug for the product group
        if groups and not platform_slug:
            platform = self.get_platform(groups[0].family.slug)

        # invalid platform, get default platform
        if not platform:
            platform = self.get_platform(default_platform_slug)
            platform_slug = default_platform_slug
            groups = None
            #products = None

        if platform:
            platform_id = platform[0].id
            if not groups:
                groups = self.get_groups(platform_id, firmware, download)
            if not platform_slug:
                platform_slug = platform[0].slug
            context['platform_slug'] = platform_slug
            #context['software'] = list(self.get_software(platform_id, software).values('file_path', 'size', 'description', 'id', 'version',).order_by('-version'))
            context['software'] = list(self.get_software(platform_id, software).values('file_path', 'size', 'description', 'id',))

        if groups:
            # group_id can be set when deeplinking to page group={productgroup.slug}
            if deeplink_group:
                group_id = deeplink_group.id
                context['group_slug'] = deeplink_group.slug
                product_downloads = self.get_downloads(deeplink_group, download)
            else:
                group_id = groups[0].id
                context['group_slug'] = groups[0].slug
                product_downloads = self.get_downloads(groups[0], download)

            if not products:
                products = self.get_models(group_id, firmware, download)
            
            context['groups'] = list(groups.values('slug', 'name', 'legacy'))
            context['downloads'] = list(product_downloads.values('name', 'slug', 'document_path', 'category__name', 'category__slug', 'thumbnail', 'thumbnail_retina'))

        if products:
            product_id = products[0].id
            product_firmwares = self.get_firmware(product_id, firmware)
            context['product_slug'] = products[0].slug
            context['products'] = list(products.values('slug', 'name', 'legacy'))
            context['firmwares'] = list(product_firmwares.values('id', 'version', 'firmware_file_path', 'size', 'changelog', 'description', 'build', 'mib', 'date_published', 'sdk__id',).order_by('-version'))

        return context

    def post(self, request, *args, **kwargs):
        ret = {}
        #update notifcation form
        if request.is_ajax() and 'email' in request.POST:
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

                print r
            except mailchimp.ListAlreadySubscribedError:
                #msg = _('You have already signed up for these updates.')
                pass
            except mailchimp.Error, e:
                #print 'An error occurred: %s - %s' % (e.__class__, e)
                pass


            #ret['msg'] = msg

        return HttpResponse(json.dumps(ret), content_type='application/json')



    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
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
            else:
                data = {
                    'groups': context['groups'],
                    'downloads': context['downloads'],
                    'products': context['products'],
                    'firmwares': context['firmwares'],
                    'software': context['software']
                }

            return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
        return super(DownloadView, self).render_to_response(context, **response_kwargs)



