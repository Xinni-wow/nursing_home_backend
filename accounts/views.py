from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser
from .serializers import RegisterSerializer, UserInfoSerializer, UserUpdateSerializer, PasswordChangeSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from common.permissions import IsStaffUserOnly

# 注册用户(仅对亲属用户开放）
@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "注册成功"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# （亲属）用户查看本人信息
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_myself_info(request):
    serializer = UserInfoSerializer(request.user)
    return Response(serializer.data)

# 查看所有亲属用户信息
@api_view(['GET'])
@permission_classes([IsStaffUserOnly])
def list_users(request):
    users = CustomUser.objects.filter(user_type='relative')
    serializer = UserInfoSerializer(users, many=True)
    return Response(serializer.data)

#  更新用户信息
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_info(request):
    serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "信息更新成功"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#  修改密码
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"msg": "密码修改成功，请重新登录"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
