from django.shortcuts import render
from django.http import JsonResponse
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
