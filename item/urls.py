
from django.urls import path
from . import views

urlpatterns = [

    path('get_subcat/', views.get_subcat, name='get_subcat'),
    path('createItem/', views.createItem, name='createItem'),
    path('wishlist_add/', views.wishlist_add, name='wishlist_add'),
    path('wishlist_delete/', views.wishlist_delete, name='wishlist_delete'),



]
