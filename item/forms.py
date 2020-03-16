from django.forms import ModelForm
from .models import *


class CreateItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('category',
                  'fond',
                  'subCategory',
                  'town',
                  'user',
                  'name',
                  'image',
                  'description',
                  'address',
                  'otherChoice',
                  'price',
                  'isService',)

class UpdateItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('category',
                  'fond',
                  'subCategory',
                  'town',
                  'user',
                  'name',
                  'image',
                  'description',
                  'address',
                  'otherChoice',
                  'price',
                  'isService',)