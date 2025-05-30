# urls.py
from django.urls import path
from .staff_views import menu_manage,menu_list

urlpatterns = [
    path('manage/', menu_manage),
    path('list/', menu_list),
    ]

