import re
from rest_framework import serializers
from accounts.models import CustomUser
from .models import Elder

# 显示老人绑定的亲属用户
class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'full_name']

class ElderSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    user= UserShortSerializer(read_only=True)

    full_name = serializers.CharField(
        max_length=50,
        error_messages={
            'required': '姓名不能为空',
            'blank': '姓名不能为空',
            'null': '姓名不能为空'
        }
    )

    id_number = serializers.CharField(
        max_length=18,
        error_messages={
            'required': '身份证号码不能为空',
            'blank': '身份证号码不能为空',
            'null': '身份证号码不能为空',
            'unique': '该身份证号码已存在，请输入其他号码'
        }
    )

    birth_date = serializers.DateField(
        error_messages={
            'required': '出生日期不能为空',
            'invalid': '请输入有效的日期格式'
        }
    )

    class Meta:
        model = Elder
        fields = ['id', 'photo', 'full_name','relationship' , 'gender', 'birth_date', 'age',
                  'id_number', 'health_status', 'notes', 'address', 'phone','user']
        # fields = '__all__'
        # read_only_fields = ['user']

    # 校验身份证号码
    def validate_id_number(self, value):
        id_pattern = r'^\d{17}[\dXx]$'
        if not re.match(id_pattern, value):
            raise serializers.ValidationError("请输入有效的18位身份证号码")

        queryset = Elder.objects.filter(id_number=value)
        instance = self.instance

        if instance:
            queryset = queryset.exclude(pk=instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("该身份证号码系统中已存在，请检查")

        return value

    # 校验电话号码（假设为中国大陆手机号）
    # def validate_phone(self, value):
    #     if value and not re.match(r'^1[3-9]\d{9}$', value):
    #         raise serializers.ValidationError("请输入有效的中国大陆手机号码")
    #     return value


    def get_age(self, obj):
        return obj.age()


    def get_photo(self, obj):
        request = self.context.get('request')
        if obj.photo and hasattr(obj.photo, 'url'):
            return request.build_absolute_uri(obj.photo.url)
        return None