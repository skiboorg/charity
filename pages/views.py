from django.shortcuts import render
from .models import *
from item.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




def index(request):

    all_categories = Category.objects.all()
    banners = Banner.objects.all()
    index_cats = all_categories.filter(atIndex=True)


    return render(request, 'pages/index.html', locals())


def catalog(request,slug):
    category = Category.objects.get(name_slug=slug)
    all_items = Item.objects.filter(category=category)
    banners = Banner.objects.all()
    data = request.GET
    print(request.GET)
    search = data.get('search')
    filter = data.get('filter')
    order = data.get('order')
    count = data.get('count')
    subcategory = data.get('subcategory')
    town = data.get('town')
    start_price = data.get('start_price')
    end_price = data.get('end_price')
    page = request.GET.get('page')
    search_qs = None
    filter_sq = None
    if search:
        items = all_items.filter(name_lower__contains=search.lower())

        if not items:
            items = all_items.filter(article__contains=search)
        search_qs = items

        param_search = search

    if filter == 'new':
        print('Поиск по фильтру туц')
        if search_qs:
            items = search_qs.filter(is_new=True)
            filter_sq = items
            param_filter = filter
        else:
            items = all_items.filter(is_new=True)
            filter_sq = items
            param_filter = filter

        param_filter = 'new'

    if filter and filter != 'new':
        print('Поиск по фильтру')

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

    if count:
        items_paginator = Paginator(items, int(count))
        param_count = count
    else:
        items_paginator = Paginator(items, 12)


    try:
        items = items_paginator.get_page(page)
    except PageNotAnInteger:
        items = items_paginator.page(1)
    except EmptyPage:
        items = items_paginator.page(items_paginator.num_pages)
    show_tags = False



    return render(request, 'pages/catalog.html', locals())


def item(request,slug):

    item = Item.objects.get(name_slug=slug)
    images = ItemImage.objects.filter(item=item)
    sameItems = Item.objects.filter(name__contains=item.name)

    return render(request, 'pages/item.html', locals())

def new_item(request):
    return render(request, 'pages/newitem.html', locals())


def login(request):

    return render(request, 'pages/login.html', locals())

def contacts(request):
    return render(request, 'pages/contacts.html', locals())
def about(request):
    return render(request, 'pages/about.html', locals())
def lk(request):
    return render(request, 'pages/lk.html', locals())