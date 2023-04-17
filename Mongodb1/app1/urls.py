from django import urls
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # path("task/", views.task, name="task"),
    # path("common/", views.common, name="common"),
    # path("get_all_data/", views.get_all_data, name="get_all_data"),
    # path("timespan/", views.timespan, name="timespan"),
    # path("get_sum/", views.get_sum, name="get_sum"),
    # path("get_avg/", views.get_avg, name="get_avg"),
    # path("get_bsavg/", views.get_bs_avg, name="get_bs_avg"),
    # path("get_sensors/", views.get_sensors, name="get_sensors"),
]
