from django.forms import ModelForm
from .models import *


class CreateItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('category',
                  'subCategory',
                  'town',
                  'user',
                  'name',
                  'description',
                  'address',
                  'price',)
