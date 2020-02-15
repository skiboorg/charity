from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from .forms import *
from .models import *
import json

def get_subcat(request):
    body = json.loads(request.body)
    return_dict = {}
    print(body)
    return_dict['subcategories'] = list()
    subcategories = SubCategory.objects.filter(category=body['category'])
    for subcat in subcategories:
         return_dict['subcategories'].append({'id':subcat.id,
                                              'name': subcat.name})
    return JsonResponse(return_dict)


def createItem(request):
    return_dict = {}
    print(request.POST)
    new_image=0
    for f in request.FILES.getlist('images'):
        print(f)
    form = CreateItemForm(request.POST)
    if form.is_valid():
        new_image = form.save()
        print(new_image.id)
    else:
        print(form.errors)
    for f in request.FILES.getlist('images'):
        ItemImage.objects.create(item_id=new_image.id,image=f).save()
    return_dict['result'] = 'success'
    # return JsonResponse(return_dict)
    return HttpResponseRedirect('/lk')

def wishlist_delete(request):
    return_dict = {}
    body = json.loads(request.body)
    return_dict = {}
    print(body)
    if request.user.is_authenticated:
        UserFavorites.objects.get(user=request.user,item_id=int(body.get('item_id'))).delete()

        return_dict['result'] = True
    else:
        return_dict['result'] = False
    return JsonResponse(return_dict)

def wishlist_add(request):
    body = json.loads(request.body)
    return_dict = {}
    print(body)
    return_dict = {}
    if request.user.is_authenticated:
        UserFavorites.objects.create(user=request.user, item_id=int(body.get('item_id')))

        return_dict['result'] = True
    else:
        return_dict['result'] = False
    return JsonResponse(return_dict)
