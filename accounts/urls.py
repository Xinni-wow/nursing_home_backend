from django.urls import path

from .views import register_user
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import get_myself_info
from .views import update_user_info
from .views import change_password
from .views import list_users

urlpatterns = [
    path('register/', register_user), # 注册
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 登录
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新
    path('user/myself/info/', get_myself_info), # 获取用户信息
    path('admin/list/', list_users),
    path('user/update/', update_user_info), # 更新用户信息
    path('user/change-password/', change_password), # 修改密码
]
