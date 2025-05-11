# from django.urls import path
#
# from .views import register_user
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
#
# from .views import get_myself_info
# from .views import update_user_info
# from .views import change_password
# from .views import list_users
#
# urlpatterns = [
#     path('auth/register/', register_user), # 注册
#     path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 登录
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新
#     path('relative/get/myinfo', get_myself_info), # 获取用户信息
#     path('staff/list/', list_users),
#     path('relative/updateme/', update_user_info), # 更新用户信息
#     path('relative/change-password/', change_password), # 修改密码
# ]
