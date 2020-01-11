from django.contrib import admin
from .models import *

class ImagesInline (admin.TabularInline):
    model = ItemImage
    extra = 0

class ItemAdmin(admin.ModelAdmin):
    inlines = [ImagesInline]
admin.site.register(Category)
admin.site.register(Banner)
admin.site.register(Item,ItemAdmin)

# Register your models here.
