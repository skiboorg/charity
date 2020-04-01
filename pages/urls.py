
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/<slug>/', views.catalog, name='catalog'),
    path('item/<slug>/', views.item, name='item'),
    path('new/', views.new_item, name='new_item'),
    path('edit/<id>', views.edit_item, name='edit_item'),
    path('delete/<id>', views.del_item, name='del_item'),



    path('login/', views.login, name='login'),
    path('lk/', views.lk, name='lk'),
    path('search/', views.search, name='search'),
    # path('profile/<nickname_req>', views.profile, name='profile'),
    # path('del_message/', views.del_message, name='del_message'),
    # path('bonus_pack/', views.bonus_pack, name='bonus_pack'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('get_fond/', views.get_fond, name='get_fond'),
    path('fonds/', views.fonds, name='fonds'),
    path('fond/<slug>', views.fond, name='fond'),
    path('payment/', views.payment, name='payment'),
    path('sber_success/', views.sber_success, name='sber_success'),
    path('sber_fail/', views.sber_fail, name='sber_fail'),
    path('documents/', views.documents, name='documents'),





    # path('statistic/', views.statistic, name='statistic'),

]
