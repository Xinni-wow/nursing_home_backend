from django.urls import path
from .views import  update_user, delete_user,search_user_combined
from .views import list_users

urlpatterns = [
    path('relatives/', list_users), # 获取全部亲属用户信息
    path('relatives/search/', search_user_combined), # 根据输入条件搜索用户信息
    path('relative/<int:pk>/update/', update_user),  # 更新用户信息
    path('relative/<int:pk>/delete/', delete_user), # 删除用户信息
]
