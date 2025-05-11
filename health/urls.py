from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HealthRecordViewSet

router = DefaultRouter()
router.register(r'records', HealthRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]