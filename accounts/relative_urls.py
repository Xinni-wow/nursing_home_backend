from django.urls import path


from .views import get_myself_info, update_myself_info,change_password

urlpatterns = [
    path('me/', get_myself_info), # 获取用户信息
    path('me/update/', update_myself_info), # 更新用户信息
    path('me/change-password/', change_password), # 修改密码
]
