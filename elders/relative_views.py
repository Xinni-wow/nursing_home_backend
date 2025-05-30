from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Elder
from .serializers import ElderSerializer
from django.db.models import ProtectedError


# 添加老人信息
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_elder(request):
    serializer = ElderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({"msg": "老人信息添加成功"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 获取当前用户所有老人
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def list_my_elders(request):
#     elders = Elder.objects.filter(user=request.user)
#     serializer = ElderSerializer(elders, many=True)
#     return Response(serializer.data)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_my_elders(request):
    elders = Elder.objects.filter(user=request.user)
    serializer = ElderSerializer(elders, many=True, context={'request': request})
    return Response(serializer.data)

# (根据id）获取单个老人详情
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def elder_detail(request, pk):
    try:
        elder = Elder.objects.get(pk=pk, user=request.user)
    except Elder.DoesNotExist:
        return Response({'error': '未找到该老人信息'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ElderSerializer(elder, context={'request': request})
    return Response(serializer.data)

# 用户修改老人信息
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_elder(request, pk):
    try:
        elder = Elder.objects.get(pk=pk, user=request.user)
    except Elder.DoesNotExist:
        return Response({'error': '老人信息不存在或无权限修改'}, status=status.HTTP_404_NOT_FOUND)

    partial = request.method == 'PATCH'
    serializer = ElderSerializer(elder, data=request.data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response({'msg': '老人信息修改成功'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 删除老人
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_elder(request, pk):
    try:
        elder = Elder.objects.get(pk=pk, user=request.user)
    except Elder.DoesNotExist:
        return Response({'error': '老人信息不存在或无权限删除'}, status=status.HTTP_404_NOT_FOUND)

    try:
        elder.delete()
    except ProtectedError:
        return Response({
            'error': '无法删除该老人，因为存在关联数据（如入住记录、健康档案等）'
        }, status=status.HTTP_400_BAD_REQUEST)

    return Response({'msg': '老人信息删除成功'}, status=status.HTTP_200_OK)
