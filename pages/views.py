import json

import requests
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import *
from item.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from item.forms import *
from chat.models import *
from customuser.forms import *

import settings


def index(request):

    all_categories = Category.objects.all()
    banners = Banner.objects.all()
    index_cats = all_categories.filter(atIndex=True)
    bestUsers = User.objects.filter(isBest=True)
    allFond = Fond.objects.all()


    return render(request, 'pages/index.html', locals())


def catalog(request, slug):
    category = get_object_or_404(Category,name_slug=slug)
    all_items = Item.objects.filter(category=category, isActive=True, isSold=False)
    print(all_items)
    if all_items:
        lower_price = all_items.order_by('price')[0].price
        high_price = all_items.order_by('-price')[0].price

    banners = Banner.objects.all()
    data = request.GET
    print(request.GET)
    search = data.get('search')
    filter = data.get('filter')
    order = data.get('order')
    count = data.get('count')
    subcat = data.get('subcategory')
    town = data.get('town')
    price_from = data.get('price_from')
    price_to = data.get('price_to')
    page = request.GET.get('page')
    search_qs = None
    filter_sq = None
    if search:
        items = all_items.filter(name_lower__contains=search.lower())

        if not items:
            items = all_items.filter(article__contains=search)
        search_qs = items

        param_search = search



    if filter:
        if search_qs:
            items = search_qs.filter(filter__name_slug=filter)
            filter_sq = items
            param_filter = filter
        else:
            items = all_items.filter(filter__name_slug=filter)
            filter_sq = items
            param_filter = filter

    if order:
        if search_qs and filter_sq:
            items = filter_sq.order_by(order)
        elif filter_sq:
            items = filter_sq.order_by(order)
        elif search_qs:
            items = search_qs.order_by(order)
        else:
            items = all_items.order_by(order)
        param_order = order

    if not search and not order and not filter:
        items = all_items
        # subcat.views = subcat.views + 1
        # subcat.save()
        param_order = '-added'

    if price_from and price_to:
        items = items.filter(Q(price__lte=price_to) & Q(price__gte=price_from))
        param_price_to = price_to
        param_price_from = price_from
        print(items)

    if subcat and subcat != '0':
        subcat_temp = SubCategory.objects.get(id=subcat)
        items = items.filter(subCategory=subcat_temp)
        param_subcat = subcat_temp.id


    if town and town != '0':
        town_temp = Town.objects.get(id=town)
        items = items.filter(town=town_temp)
        param_town = town_temp.id
    filtered_items_count = len(items)

    if count:
        items_paginator = Paginator(items, int(count))
        param_count = count
    else:
        items_paginator = Paginator(items, 9)
    print(len(items))

    try:
        items = items_paginator.get_page(page)
    except PageNotAnInteger:
        items = items_paginator.page(1)
    except EmptyPage:
        items = items_paginator.page(items_paginator.num_pages)
    show_tags = False



    return render(request, 'pages/catalog.html', locals())


def item(request,slug):

    item = get_object_or_404(Item,name_slug=slug)
    images = ItemImage.objects.filter(item=item)
    sameItems = Item.objects.filter(name__contains=item.name)
    allFonds = Fond.objects.all()

    return render(request, 'pages/item.html', locals())

def new_item(request):
    form = CreateItemForm()
    allFonds = Fond.objects.all()

    return render(request, 'pages/newitem.html', locals())

def edit_item(request,id):
    item = Item.objects.get(id=id)
    if item.user.id == request.user.id:
        form = UpdateItemForm()
        allFonds = Fond.objects.all()
        return render(request, 'pages/itemedit.html', locals())
    else:
        return render(request, 'pages/index.html', locals())

def del_item(request,id):
    item = Item.objects.get(id=id)
    if item.user.id == request.user.id:
        item.delete()
        allFonds = Fond.objects.all()
        return HttpResponseRedirect('/lk/')
    else:
        return render(request, 'pages/index.html', locals())

def login(request):

    return render(request, 'pages/login.html', locals())

def contacts(request):
    return render(request, 'pages/contacts.html', locals())
def about(request):
    return render(request, 'pages/about.html', locals())
def lk(request):
    if request.user.is_authenticated:
        user = request.user
        updateForm = UpdateForm()
        userItems = Item.objects.filter(user=user, isSold=False)
        soldItems = Item.objects.filter(user=user, isSold=True)
        wl = UserFavorites.objects.filter(user=user)
        wishlist_ids = []
        for i in wl:
            wishlist_ids.append(i.item.id)
        userFavs = Item.objects.filter(id__in=wishlist_ids)
        lkActive = True

        allChats = Chat.objects.filter(users__in=[user.id])
        print(allChats)
        allUnreadChats = allChats.filter(isNewMessages=True)
        allReadChats = allChats.filter(isNewMessages=False)
        allBuys = UserBuys.objects.filter(user=user)
        print('allUnreadChats', allUnreadChats)
        print('allReadChats', allReadChats)
        print('allBuys', allBuys)
        allChatPeoples = []
        for x in allChats:
            for y in x.users.all():
                print(y.id)
                if y.id != request.user.id:
                    allChatPeoples.append(User.objects.get(id=y.id))
        print(allChatPeoples)

        return render(request, 'pages/lk.html', locals())
    else:
        return render(request, 'pages/index.html', locals())


def search(request):
    show_tags = False
    search_string = request.GET.get('query')
    category = request.GET.get('category')
    town = request.GET.get('town')
    page = request.GET.get('page')
    param_search = search_string

    searchResult = Item.objects.filter(name_lower__contains=search_string.lower())

    if searchResult:
        if category:
            cat = get_object_or_404(Category,id=category)
            searchResult = searchResult.filter(category=cat)
        if town:
            townn = get_object_or_404(Town,id=town)
            searchResult = searchResult.filter(town=townn)

    return render(request, 'pages/search.html', locals())

def get_fond(request):
    return_dict = {}
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    fond = Fond.objects.get(id=body['fond_id'])
    return_dict['fond_info'] = fond.description_short
    return JsonResponse(return_dict, safe=False)


def fonds(request):
    allFonds = Fond.objects.all()
    return render(request, 'pages/fonds.html', locals())

def fond(request,slug):
    fond = get_object_or_404(Fond, name_slug=slug)
    return render(request, 'pages/fond.html', locals())

def payment(request):
    item_id = request.POST.get('id')
    print(item_id)
    item = get_object_or_404(Item,id=item_id)
    new_order = Order.objects.create(seller=item.user,
                                     buyer=request.user,
                                     item=item,
                                     pay_by='Сбербанк')

    orderBundle = {
        "customerDetails": {"phone": "79998887766", "email": "mail@mail.ru", "fullName": "", "passport": "123","inn": "1231231231"},
        "cartItems":
        {"items":
            [
                {"positionId": 1,
                 "name": item.name,
                 "quantity": {"value": 1,"measure":'шт'},
                 "itemAmount": int(f'{item.price}00'),
                 "itemCode": item.name_slug,
                 "tax": {"taxType": 0,'taxSum': 0},
                 "itemPrice": int(f'{item.price}00'),
                 'itemAttributes':
                     {'attributes':
                         [
                             {'name': 'paymentMethod', 'value': 1},
                             {'name': 'paymentObject', 'value': 4 if item.isService else 1},
                             {'name': 'agent_info.type', 'value': 3}
                         ]
                     }
                 }
            ]
        }
    }
    o={"cartItems":{"items":[{"positionId":1,"name":"Дезодорант 1","quantity":{"value":1,"measure":"шт"},"itemCode":"51","itemPrice":55550,"itemAmount":55550, "tax":{"taxType":0, "taxSum":0}}]}}
    print('ww')
    print(orderBundle)
    response = requests.get('https://securepayments.sberbank.ru/payment/rest/register.do?'
                            f'amount={item.price}00&'
                            f'orderNumber={str(new_order.id) + "-" + "".join(choices(string.ascii_lowercase + string.digits, k=2))}&'
                            f'description=Покупка {"услуги" if item.isService else "товара"} №{item.id}&'
                            f'password={settings.SBER_PASSWORD}&'
                            f'userName={settings.SBER_LOGIN}&'
                            f'returnUrl={settings.SBER_SUCCESS_URL}&'
                            f'failUrl={settings.SBER_FAIL_URL}&'
                            'pageView=DESKTOP&sessionTimeoutSecs=1200&taxSystem=1&'
                            # 'additionalOfdParams":'
                            # '{"agent_info.type":"3"},'
                            # '{"supplier_info.name":"Inoy"}&'
                            'orderBundle={'
                            '"cartItems":{'
                            '"items":['
                            '{"positionId":1,'
                            f'"name":"{item.name}",'
                            '"quantity":{'
                            '"value": 1,'
                            '"measure":"шт"},'
                            f'"itemCode":"{item.name_slug}",'
                            f'"itemPrice":{item.price}00,'
                            f'"itemAmount":{item.price}00,'
                            '"tax":{"taxType":0,"taxSum":0},'
                            '"itemAttributes": '
                            '{"attributes": ['
                            # '{"supplier_info.phones":["+78000000000"]},'
                            '{"name":"agent_info.type", "value":"3"},'
                            '{"name":"supplier_info.name", "value":"00000000"},'
                            '{"name":"supplier_info.inn", "value":"000000000000"},'
                            '{"name": "paymentMethod", "value": 1},'
                            '{"name": "paymentObject",'
                            f'"value": {4 if item.isService else 1}'
                            '}]}'                            
                            '}]}}')

    # response = requests.get('https://securepayments.sberbank.ru/payment/rest/register.do?'
    #                         f'amount={item.price}00&'
    #                         f'orderNumber={str(new_order.id) + "-" + "".join(choices(string.ascii_lowercase + string.digits, k=2))}&'
    #                         f'description=Покупка {"услуги" if item.isService else "товара"} №{item.id}&'
    #                         f'password={settings.SBER_PASSWORD}&'
    #                         f'userName={settings.SBER_LOGIN}&'
    #                         f'returnUrl={settings.SBER_SUCCESS_URL}&'
    #                         f'failUrl={settings.SBER_FAIL_URL}&'
    #                         'pageView=DESKTOP&sessionTimeoutSecs=1200&taxSystem=1&'
    #                         'orderBundle={'
    #                         '"cartItems":{'
    #                         '"items":['
    #                         '{"positionId":1,'
    #                         f'"name":"{item.name}",'
    #                         '"quantity":{'
    #                         '"value": 1,'
    #                         '"measure":"шт"},'
    #                         f'"itemCode":"{item.name_slug}",'
    #                         f'"itemPrice":{item.price}00,'
    #                         f'"itemAmount":{item.price}00,'
    #                         '"tax":{"taxType":0,"taxSum":0},'
    #                         '"itemAttributes": '
    #                         '{"attributes": [{"name": "paymentMethod", "value": 1},'
    #                         '{"name": "paymentObject",'
    #                         f'"value": {4 if item.isService else 1},'
    #                         '{"name": "agent_info.type", "value": 3}'
    #
    #
    #                         '}]}'
    #                         '}]}}')
    print(json.loads(response.content))
    response_data = json.loads(response.content)
    print('formUrl', response_data)

    try:
        orderId = response_data['orderId']
        new_order.sber_orderID = orderId
        new_order.save()
        print('orderId', orderId)
        print('formUrl', response_data['formUrl'])
        return HttpResponseRedirect(response_data['formUrl'])
    except:
        print('error')

    pass

def sber_success(request):
    sber_orderId = request.GET.get('orderId')
    order = get_object_or_404(Order, sber_orderID=sber_orderId)
    item = order.item
    order.isPayed = True
    UserBuys.objects.create(user=order.buyer,item=item)
    item.isSold = True
    if item.fond:
        item.fond.money_earn += item.price
        item.fond.save()
    item.save()
    order.save()
    return render(request, 'pages/order_complete.html', locals())

def sber_fail(request):
    return render(request, 'pages/order_fail.html', locals())

def documents (request):
    return render(request, 'pages/documents.html', locals())
