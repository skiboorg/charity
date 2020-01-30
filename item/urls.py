
from django.urls import path
from . import views

urlpatterns = [

    path('get_subcat/', views.get_subcat, name='get_subcat'),



]
