from django.urls import path
from .staff_views import list_elders, search_elders, elder_detail,update_elder,delete_elder

urlpatterns = [
    path('', list_elders),  # 查看我家老人
    path('search/',search_elders),  # 搜索老人
    path('<int:pk>/', elder_detail) ,# 查看老人详细信息
    path('<int:pk>/update/', update_elder),
    path('<int:pk>/delete/', delete_elder),# 删除老人

]
