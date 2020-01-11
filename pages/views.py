from django.shortcuts import render
from .models import *

def index(request):

    all_categories = Category.objects.all()
    banners = Banner.objects.all()
    index_cats = all_categories.filter(atIndex=True)


    return render(request, 'pages/index.html', locals())


def catalog(request,id):
    cat = Category.objects.get(id=id)
    banners = Banner.objects.all()
    all_categories = Category.objects.all()

    return render(request, 'pages/catalog.html', locals())
def item(request,id):
    all_categories = Category.objects.all()
    item = Item.objects.get(id=id)
    images = ItemImage.objects.filter(item=item)

    return render(request, 'pages/item.html', locals())