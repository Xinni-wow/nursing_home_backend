from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status

from elders.models import Elder
from .models import CustomUser
from .serializers import RegisterSerializer, UserInfoSerializer, UserUpdateSerializer, PasswordChangeSerializer


from rest_framework.permissions import IsAuthenticated
from common.permissions import IsStaffUserOnly


from django.db import IntegrityError
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# 登录
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# 注册用户(仅对亲属用户开放）
@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "注册成功"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 找回密码
@api_view(['POST'])
def retrieve_security_question(request):
    username = request.data.get('username')
    try:
        user = CustomUser.objects.get(username=username)
        if user.user_type != 'relative':
            return Response({
                'msg': '找回密码仅限家属用户，工作人员请联系系统超级管理员修改密码。'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not user.security_question:
            return Response({
                'code': 400,
                'msg': '未设置密保问题，请联系系统超级管理员修改新密码'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({'security_question': user.security_question}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'message': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def reset_password(request):
    username = request.data.get('username')
    security_answer = request.data.get('security_answer')
    new_password = request.data.get('new_password')
    try:
        user = CustomUser.objects.get(username=username)
        if user.user_type != 'relative':
            return Response({'msg': '找回密码仅限家属用户，工作人员请联系系统超级管理员修改密码。'}, status=status.HTTP_400_BAD_REQUEST)
        if user.security_answer != security_answer:
            return Response({'msg': '密保答案错误'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({'msg': '密码重置成功'}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'msg': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

# (亲属用户)查看本人信息
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_myself_info(request):
    serializer = UserInfoSerializer(request.user)
    return Response(serializer.data)

# （亲属用户）更新个人信息
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_myself_info(request):
    serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"detail": "信息更新成功"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#  修改密码（还没用上）
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

# (管理员)查看所有亲属用户信息
@api_view(['GET'])
@permission_classes([IsStaffUserOnly])
def list_users(request):
    users = CustomUser.objects.filter(user_type='relative')
    serializer = UserInfoSerializer(users, many=True)
    return Response(serializer.data)

# (管理员)根据用户名查找用户
# @api_view(['GET'])
# @permission_classes([IsStaffUserOnly])
# def search_user(request, username):
#     users = CustomUser.objects.filter(user_type='relative',username__icontains=username)
#     serializer = UserInfoSerializer(users, many=True)
#     return Response(serializer.data)
@api_view(['GET'])
@permission_classes([IsStaffUserOnly])
def search_user(request):
    username = request.GET.get('username')

    if not username:
        return Response({"error": "缺少 username 参数"}, status=400)

    users = CustomUser.objects.filter(user_type='relative', username__icontains=username)
    serializer = UserInfoSerializer(users, many=True)
    return Response(serializer.data)


# (管理员)根据真实姓名查找用户
@api_view(['GET'])
@permission_classes([IsStaffUserOnly])
def search_user_by_name(request):
    # 从查询参数中获取 name
    name = request.GET.get('name')
    if not name:
        return Response({"error": "缺少 name 参数"}, status=400)
    users = CustomUser.objects.filter(user_type='relative', full_name__icontains=name)
    serializer = UserInfoSerializer(users, many=True)
    return Response(serializer.data)

# (管理员)更新用户信息
@api_view(['PUT', 'PATCH'])
@permission_classes([IsStaffUserOnly])
def update_user(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk, user_type='relative')
    except CustomUser.DoesNotExist:
        return Response({'error': '用户不存在'}, status=404)

    partial = request.method == 'PATCH'
    serializer = UserInfoSerializer(user, data=request.data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response({'msg': '用户信息更新成功'})
    return Response(serializer.errors, status=400)

# （管理员）删除用户
from django.db.models import ProtectedError

@api_view(['DELETE'])
@permission_classes([IsStaffUserOnly])
def delete_user(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk, user_type='relative')
        user.delete()
        return Response({'msg': '用户已删除'})
    except CustomUser.DoesNotExist:
        return Response({'error': '用户不存在'}, status=404)
    except ProtectedError:
        return Response({'error': '该用户已绑定老人信息，无法删除'}, status=400)


@api_view(['GET'])
@permission_classes([IsStaffUserOnly])
def search_user_by_elder_name(request):
    elder_name = request.GET.get('elder_name')
    if not elder_name:
        return Response({"error": "缺少 elder_name 参数"}, status=400)

    # 查找绑定该老人姓名的用户
    elders = Elder.objects.filter(full_name__icontains=elder_name)
    user_ids = elders.values_list('user_id', flat=True).distinct()
    users = CustomUser.objects.filter(id__in=user_ids, user_type='relative')
    serializer = UserInfoSerializer(users, many=True)
    return Response(serializer.data)
