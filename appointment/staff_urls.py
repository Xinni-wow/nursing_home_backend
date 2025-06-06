from django.urls import path
from .staff_views import visit_list, review_visit_request

urlpatterns = [
    path('list/', visit_list),
    path('review/<int:pk>/', review_visit_request),
]

# 主urls.py中配置
# path('api/staff/visit/', include('visits.staff_urls')),