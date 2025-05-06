from django.urls import path
from .views import add_elder,list_my_elders, elder_detail,update_elder

urlpatterns = [
    path('add/', add_elder),
    path('my/', list_my_elders),
    path('<int:pk>/', elder_detail),
    path('<int:pk>/update/', update_elder),
]
