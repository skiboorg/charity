from django.shortcuts import render, get_object_or_404
from .models import *
from item.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from item.forms import *




def index(request):

    all_categories = Category.objects.all()
    banners = Banner.objects.all()
    index_cats = all_categories.filter(atIndex=True)


    return render(request, 'pages/index.html', locals())


def catalog(request, slug):
    category = get_object_or_404(Category,name_slug=slug)
    all_items = Item.objects.filter(category=category)
    lower_price = all_items.order_by('price')[0].price
    high_price = all_items.order_by('-price')[0].price
    print('lower_price',lower_price)
    print('high_price', high_price)
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

    return render(request, 'pages/item.html', locals())

def new_item(request):
    form = CreateItemForm()
    return render(request, 'pages/newitem.html', locals())


def login(request):

    return render(request, 'pages/login.html', locals())

def contacts(request):
    return render(request, 'pages/contacts.html', locals())
def about(request):
    return render(request, 'pages/about.html', locals())
def lk(request):
    if request.user.is_authenticated:
        user = request.user
        userItems = Item.objects.filter(user=user)
        wl = UserFavorites.objects.filter(user=request.user)
        wishlist_ids = []
        for i in wl:
            wishlist_ids.append(i.item.id)
        userFavs = Item.objects.filter(id__in=wishlist_ids)
        lkActive = True
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