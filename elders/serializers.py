from rest_framework import serializers
from .models import Elder

class ElderSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = Elder
        fields = ['id', 'photo', 'full_name', 'gender', 'birth_date', 'age',
                  'id_number', 'health_status', 'notes', 'address', 'phone']

    def get_age(self, obj):
        return obj.age()
