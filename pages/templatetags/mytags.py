
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
    item = UserBuys.objects.get(item_id=data.id)
    print(item)
    return (f'Дата продажи: {item.createdAt}<br>'
            f'Покупатель: {item.user.name}<br><br>'
            f' <span style="cursor: pointer; text-decoration: underline;" onclick="startChat({item.item.user.id},{item.user.id},{item.item.id})">Начать чат</span>')
