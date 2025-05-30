import re
from rest_framework import serializers

from elders.models import Elder
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
# 用户登录
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 添加自定义声明
        token['username'] = user.username
        token['user_type'] = user.user_type
        token['email'] = user.email

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # 添加额外用户信息到响应体中
        data['user_info'] = {
            'id': self.user.id,
            'username': self.user.username,
            'user_type': self.user.user_type,
            'full_name': self.user.full_name,
            'phone': self.user.phone,
            'address': self.user.address,
            'email': self.user.email,
        }
        # data['status'] = 'success'
        # data['message'] = 'Login successful'

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# 用户注册
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        # 禁用默认的 UniqueValidator，可以自定义提示语
        validators=[],
    )
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    full_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    security_question = serializers.CharField(required=True)
    security_answer = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password2', 'full_name', 'phone', 'address', 'email','security_question', 'security_answer']

    def validate(self, attrs):
        # 用户名重复检查
        if CustomUser.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "该用户名已存在"})

        # 密码一致性校验
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password2": "两次输入的密码不一致"})

        # 密码强度检查（使用 django 自带）
        try:
            validate_password(attrs['password'])
        except DjangoValidationError:
            raise serializers.ValidationError({"password": "密码不符合要求，至少8位，包含字母和数字，不能过于常见"})

        return attrs

    # 校验手机号
    def validate_phone(self, value):
        if value and not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError("请输入有效的中国大陆手机号码")
        return value

    # 校验邮箱（如果有的话）
    def validate_email(self, value):
        if value and not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
            raise serializers.ValidationError("请输入有效的邮箱地址")
        return value

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create(
            username=validated_data['username'],
            full_name=validated_data['full_name'],
            phone=validated_data['phone'],
            address=validated_data['address'],
            email=validated_data.get('email', ''),
            user_type='relative', # 注册接口只能创建亲属
            security_question=validated_data['security_question'],
            security_answer=validated_data['security_answer'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# 显示用户绑定的老人
class ElderSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elder
        fields = ['id', 'full_name', 'relationship']

# 查看用户信息
class UserInfoSerializer(serializers.ModelSerializer):
    elders = ElderSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'full_name', 'phone', 'address', 'email', 'user_type','elders']

# 修改用户信息
class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[]  # 禁用默认的 UniqueValidator，我们可以自定义处理
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'phone', 'address', 'email']

    def validate_username(self, value):
        user = self.instance  # 当前正在更新的用户对象
        if CustomUser.objects.filter(username=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("该用户名已存在，请换一个用户名")
        return value



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

