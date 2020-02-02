from django.urls import path
from . import views

urlpatterns = [
   path('login_req/', views.login_req, name='login_req'),
   path('logout/', views.logout_page, name='logout'),
   path('reg_req', views.reg_req, name='reg_req'),
   path('update_req', views.update_req, name='update_req'),
]
