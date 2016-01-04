from django.conf.urls import patterns, url

from .views import DownloadView, DownloadCountView, search_autocomplete

urlpatterns = patterns('',
    url(r'^$', DownloadView.as_view(), name='download'),
    url(r'^autocomplete/$', search_autocomplete, name='download-autocomplete'),
    url(r'^search/$', DownloadView.as_view(search=True), name='download-search'),
    url(r'^track/$', DownloadCountView.as_view(), name='download-count'),

    url(r'^(?P<platform>[-_\w]+)/?(?P<product_group>[-_\w]+)?/?(?P<product_model>[-_\w]+)?/?(?P<product_item>[-_\w]+)?/$', 
        DownloadView.as_view(), name='download-deeplink'),
)