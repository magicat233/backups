import os
from django import template
from django.conf import settings

register = template.Library()

@register.filter
def filename(value):
    return os.path.basename(value)


@register.filter
def downloadUrl(value):
    if value.startswith(('http://', 'https://'),):
        return value
    return '/downloads/' + value