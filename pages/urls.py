
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/<id>/', views.catalog, name='catalog'),
    path('item/<id>/', views.item, name='item'),



    path('login/', views.login, name='login'),
    path('lk/', views.lk, name='lk'),
    # path('profile/<nickname_req>', views.profile, name='profile'),
    # path('del_message/', views.del_message, name='del_message'),
    # path('bonus_pack/', views.bonus_pack, name='bonus_pack'),
    # path('about_us/', views.about_us, name='about_us'),
    # path('rules/', views.rules, name='rules'),
    # path('add_to_player_balance/', views.add_to_player_balance, name='add_to_player_balance'),
    # path('about_bonus_pack/', views.about_bonus_pack, name='about_bonus_pack'),




    # path('statistic/', views.statistic, name='statistic'),

]
