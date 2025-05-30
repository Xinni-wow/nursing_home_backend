from django.urls import path

from .views import register_user, CustomTokenObtainPairView, retrieve_security_question, reset_password
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/', register_user), # 注册(仅对用户开放）
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # 登录
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新
    path('retrieve_security_question/', retrieve_security_question, name='retrieve_security_question'),
    path('reset_password/', reset_password, name='reset_password'),
]

