# outing/relative_urls.py
from django.urls import path,include
from .relative_views import add_outing_request, list_user_outings, outing_request_detail, cancel_outing_request

urlpatterns = [
    path('add/', add_outing_request),
    path('list/', list_user_outings),
    path('<int:pk>/', outing_request_detail),
    path('<int:pk>/cancel/', cancel_outing_request),
]

# 主urls.py
path('api/relative/outing/', include('outing.relative_urls')),
