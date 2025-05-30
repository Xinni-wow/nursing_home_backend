from rest_framework import serializers
from .models import OutingRequest
from elders.models import Elder
from elders.models import Elder
from rest_framework import serializers
from elders.serializers import ElderSerializer

class OutingRequestSerializer(serializers.ModelSerializer):
    elder = ElderSerializer(read_only=True)  # 用于返回时嵌套显示
    elder_id = serializers.PrimaryKeyRelatedField(
        queryset=Elder.objects.all(), write_only=True, source='elder'
    )
    is_approved = serializers.SerializerMethodField()

    class Meta:
        model = OutingRequest
        fields = [
            'id',
            'elder',
            'elder_id',  # 前端用这个提交
            'start_time',
            'end_time',
            'reason',
            'status',
            'is_approved',
            'remarks',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['status', 'is_approved', 'created_at', 'updated_at', 'elder']

    def get_is_approved(self, obj):
        return obj.status == 'approved'

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("开始时间必须早于结束时间")
        return data
