from .models import Room, CheckIn, Bill
from datetime import date
from elders.models import Elder
from rest_framework import serializers

class ElderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elder
        fields = ['id', 'full_name']

# 房间序列化器（用于获取空房间列表）
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_number', 'capacity', 'is_occupied']

# 入住序列化器
class CheckInSerializer(serializers.ModelSerializer):
    elder_name = serializers.CharField(source='elder.full_name', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)

    def get_elder_name(self, obj):
        return obj.elder.full_name

    def get_room_number(self, obj):
        return obj.room.room_number

    class Meta:
        model = CheckIn
        fields = ['id', 'elder', 'room', 'start_date', 'duration_years', 'status', 'checkin_date', 'elder_name', 'room_number']
        read_only_fields = ['stay_fee', 'meal_fee', 'total_fee', 'checkin_date', 'elder_name', 'room_number']  # 告诉它这些字段不需要用户输入

    def validate_start_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("入住日期不能早于今天")
        return value


    def validate(self, data):
        elder = data['elder']
        room = data['room']

        # 判断老人是否已在住
        if CheckIn.objects.filter(elder=elder, status='active').exists():
            raise serializers.ValidationError("该老人已办理入住，不能重复入住。")

        # 判断房间是否已满
        current_occupants = CheckIn.objects.filter(room=room, status='active').count()
        if current_occupants >= room.capacity:
            raise serializers.ValidationError(f"房间 {room.room_number} 已满，无法入住。")

        return data

    def create(self, validated_data):
        duration = validated_data['duration_years']
        validated_data['status'] = 'active'
        return super().create(validated_data)

class BillSerializer(serializers.ModelSerializer):
    elder_name = serializers.CharField(source='elder.full_name', read_only=True)
    room_number = serializers.CharField(source='checkin.room.room_number', read_only=True)

    class Meta:
        model = Bill
        fields = [
            'id', 'elder', 'elder_name', 'room_number',
            'checkin', 'years',
            'stay_fee', 'meal_fee', 'total_fee',
            'type', 'created_at'
        ]