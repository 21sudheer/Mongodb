from django import urls
from django.urls import path
from . import views

urlpatterns=[
    path('cvs/', views.cvs, name='cvs'),
    path('cal/', views.cal, name='cal'),
    path('info/', views.info, name='info'),
    path('get_sum/', views.get_sum, name='get_sum'),
    path('get_avg/', views.get_avg, name='get_avg'),
    path('get_bsavg/', views.get_bs_avg, name='get_bs_avg'),
    path('get_sensors/', views.get_sensors, name='get_sensors'),

]