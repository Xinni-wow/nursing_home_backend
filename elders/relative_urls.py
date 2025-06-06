from django.urls import path
from .relative_views import add_elder, list_my_elders, elder_detail, update_elder,delete_elder

urlpatterns = [
    path('add/', add_elder), # 添加老人
    path('', list_my_elders),# 查看我家老人
    path('<int:pk>/', elder_detail),# 查看我家老人详细信息
    path('<int:pk>/update/', update_elder),# 修改老人信息
    path('<int:pk>/delete/', delete_elder),# 删除老人
]