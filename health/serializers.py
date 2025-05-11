from rest_framework import serializers
from .models import HealthRecord
from elders.models import Elder


class ElderSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elder
        fields = ['id', 'full_name']

class HealthRecordSerializer(serializers.ModelSerializer):
    elder = serializers.PrimaryKeyRelatedField(queryset=Elder.objects.all())  # 可接收 elder 的 ID
    elder_info = ElderSimpleSerializer(source='elder', read_only=True)
    date = serializers.DateField(required=True)

    class Meta:
        model = HealthRecord
        fields = '__all__'
        read_only_fields = ['created_at']
