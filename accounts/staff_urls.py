from django.urls import path

from .views import search_user, search_user_by_name, update_user, delete_user, search_user_by_elder_name
from .views import list_users

urlpatterns = [
    path('relatives/', list_users), # 获取全部亲属用户信息
    path('relatives/search-by-username/', search_user),
    path('relatives/search-by-fullname/', search_user_by_name),
    path('relative/<int:pk>/update/', update_user),  # 更新用户信息
    path('relative/<int:pk>/delete/', delete_user),
    path('relative/search-by-elder/', search_user_by_elder_name),
]
