from rest_framework import serializers
from .models import VisitRequest


class VisitRequestSerializer(serializers.ModelSerializer):
    elder_name = serializers.CharField(source='elder.full_name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)  # 新增
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = VisitRequest
        fields = [
            'id', 'elder', 'elder_name', 'user', 'user_name', 'user_full_name',  # 新增user_full_name
            'visit_date', 'visit_time', 'visitor_count', 'reason',
            'status', 'status_display', 'remarks', 'qr_code',
            'qr_code_expiry', 'created_at'
        ]
        extra_kwargs = {
            'elder': {'required': True},
            'visit_date': {'required': True},
            'visit_time': {'required': True},
            'reason': {'required': True},
            'user': {'read_only': True},
        }
