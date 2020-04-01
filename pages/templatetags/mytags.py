
from django import template
from item.models import UserBuys
from pytils.translit import slugify

register = template.Library()


@register.filter
def slice_qs(data):
    print(data)
    return

@register.filter
def get_sold_info(data):
    print('get_sold_info')
    print(data.id)
    item = UserBuys.objects.get(item=data)
    print(item)
    return (f'Дата продажи: {item.createdAt}<br>'
            f'Покупатель: {item.user.name}')
