from django.conf.urls import patterns, url

from .views import DownloadView

urlpatterns = patterns('',
    url(r'^$', DownloadView.as_view(), name='download'),

    url(r'^(?P<platform>airfiber)/$', DownloadView.as_view(), name='download-airfiber'),
    url(r'^(?P<platform>airmax)/$', DownloadView.as_view(), name='download-airmax'),
    url(r'^(?P<platform>edgemax)/$', DownloadView.as_view(), name='download-edgemax'),
    url(r'^(?P<platform>unifi)/$', DownloadView.as_view(), name='download-unifi'),
    url(r'^(?P<platform>unifi-video)/$', DownloadView.as_view(), name='download-unifi-video'),
    url(r'^(?P<platform>unifivideo)/$', DownloadView.as_view(), name='download-unifivideo'),
    url(r'^(?P<platform>airvision)/$', DownloadView.as_view(), name='download-airvision'),
    url(r'^(?P<platform>mfi)/$', DownloadView.as_view(), name='download-mfi'),
    url(r'^(?P<platform>accessories)/$', DownloadView.as_view(), name='download-accessories'),

    #url(r'^(?P<platform>[-_\w]+)/$', DownloadView.as_view(), name='download-platform'),
    url(r'^track/$', DownloadView.as_view(), name='download-count'),
    url(r'^(?P<platform>[-_\w]+)/?(?P<product_group>[-_\w]+)?/?(?P<product_model>[-_\w]+)?/?(?P<product_item>[-_\w]+)?/$', 
        DownloadView.as_view(), name='download-deeplink'),
)