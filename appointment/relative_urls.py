from django.urls import path
from .relative_views import (
    add_visit_request,
    list_user_visits,
    visit_request_detail,
    cancel_visit_request,
    get_visit_qrcode,
    visit_detail
)

urlpatterns = [
    path('add/', add_visit_request),
    path('list/', list_user_visits),
    path('<int:pk>/cancel/', cancel_visit_request),
    path('<int:pk>/qrcode/', get_visit_qrcode),
    path('<int:pk>/', visit_detail),


]

# 主urls.py中配置
# path('api/relative/visit/', include('visits.relative_urls')),