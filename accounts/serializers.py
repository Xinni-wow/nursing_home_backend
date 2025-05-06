from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password

# 用户注册
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    full_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    email = serializers.EmailField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password2', 'full_name', 'phone', 'address', 'email']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "两次输入的密码不一致"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create(
            username=validated_data['username'],
            full_name=validated_data['full_name'],
            phone=validated_data['phone'],
            address=validated_data['address'],
            email=validated_data.get('email', ''),
            user_type='relative',  # 注册接口只能创建亲属
        )
        user.set_password(validated_data['password'])  # 加密密码
        user.save()
        return user

# 查看用户信息
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'full_name', 'phone', 'address', 'email', 'user_type']

# 修改用户信息
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'phone', 'address', 'email']

# 修改密码
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("原密码错误")
        return value

    def validate_new_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("新密码至少 6 位")
        return value
