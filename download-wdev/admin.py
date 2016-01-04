from django.contrib import admin
from .models import DownloadCategory, Download, DownloadSubscriber

class DownloadAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'category', 'get_product_groups', 'document_path', 'is_legacy')
    list_filter = ('category', 'product_group',)
    #list_editable = ('document_path',)

    class Media:
        js = (
            'bower_components/jquery/dist/jquery.min.js',
            'scripts/helpers/admin/download.js',
        )

class DownloadCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'order', )



admin.site.register(DownloadCategory, DownloadCategoryAdmin)
admin.site.register(Download, DownloadAdmin)
admin.site.register(DownloadSubscriber)