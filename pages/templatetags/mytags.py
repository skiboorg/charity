
from django import template
from pytils.translit import slugify

register = template.Library()


@register.filter
def slice_qs(data):
    print(data)
    return

