from django.contrib import admin
from .models import DownloadCategory, Download


class DownloadAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('sdk',)
    list_display = (
        'name', 'category', 'product_family', 'get_product_groups_for_admin', 'get_product_models_for_admin', 'file_path', 'is_legacy')
    list_filter = ('category', 'product_groups',)
    search_fields = ['name', 'file_path']

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
