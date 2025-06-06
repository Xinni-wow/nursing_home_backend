# outing/relative_urls.py
# outing/staff_urls.py

from django.urls import path ,include
from .staff_views import review_outing_request ,outing_list

urlpatterns = [

    path('review/<int:pk>/', review_outing_request),  # PUT 有 pk，审批指定申请
    path('list/', outing_list),   # 新增列表接口
]
path('api/staff/outing/', include('outing.staff_urls')),
