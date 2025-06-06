from rest_framework import serializers
from .models import DailyMenu
class DailyMenuSerializer(serializers.ModelSerializer):
    meal_type_display = serializers.CharField(source='get_meal_type_display', read_only=True)

    class Meta:
        model = DailyMenu
        fields = ['id', 'date', 'meal_type', 'meal_type_display', 'content']

    def validate(self, attrs):
        # 不调用父类的validate，不触发unique校验
        return attrs
