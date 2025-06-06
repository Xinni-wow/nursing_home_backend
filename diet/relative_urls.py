from .relative_views import user_menu_view
from django.urls import path

urlpatterns = [
    path('menu/', user_menu_view, name='user_menu' ),

]
