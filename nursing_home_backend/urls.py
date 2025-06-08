"""
URL configuration for nursing_home_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls), # 超级后台管理员

    # 登录和个人信息
    path('api/auth/', include('accounts.auth_urls')),
    path('api/relative/', include('accounts.relative_urls')),#（亲属）用户端
    path('api/staff/', include('accounts.staff_urls')),#（工作人员）管理端)

    # 老人管理模块
    path('api/relative/elders/', include('elders.relative_urls')),#（亲属）用户端
    path('api/staff/elders/', include('elders.staff_urls')),#（工作人员）管理端

    #health
    path('api/health/', include('health.urls')),
    #outing(外出申请)
    path('api/relative/outing/',include('outing.relative_urls')),
    path('api/staff/outing/',include('outing.staff_urls')),
    #appointment（预约）
    path('api/relative/appointment/',include('appointment.relative_urls')),
    path('api/staff/appointment/',include('appointment.staff_urls')),
    #diet（饮食）
    path('api/relative/diet/',include('diet.relative_urls')),
    path('api/staff/diet/',include('diet.staff_urls')),

    #入住办理，缴费
    path('api/', include('checkin.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 登录接口
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新 token
    path('api/', include('checkin.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)