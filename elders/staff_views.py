from django.db.models import ProtectedError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from common.permissions import IsStaffUserOnly
from .models import Elder
from .serializers import ElderSerializer

# 获取所有老人
@api_view(['GET'])
@permission_classes([IsStaffUserOnly])
def list_elders(request):
    elders = Elder.objects.all()
    serializer = ElderSerializer(elders, many=True,context={'request': request})
    return Response(serializer.data)

# 搜索老人
@api_view(['GET'])
@permission_classes([IsStaffUserOnly])
def search_elders(request):
    name = request.GET.get('name')
    if not name:
        return Response({"error": "缺少 name 参数"}, status=400)
    elders = Elder.objects.filter(full_name__icontains=name)
    serializer = ElderSerializer(elders, many=True,context={'request': request})
    return Response(serializer.data)

# 获取老人详情
@api_view(['GET'])
@permission_classes([IsStaffUserOnly])
def elder_detail(request, pk):
    try:
        elder = Elder.objects.get(pk=pk)
    except Elder.DoesNotExist:
        return Response({"error": "未找到老人"}, status=404)

    serializer = ElderSerializer(elder,context={'request': request})
    return Response(serializer.data)

# 编辑老人
@api_view(['PUT', 'PATCH'])
@permission_classes([IsStaffUserOnly])
def update_elder(request, pk):
    try:
        elder = Elder.objects.get(pk=pk)
    except Elder.DoesNotExist:
        return Response({"error": "未找到老人"}, status=404)

    serializer = ElderSerializer(elder, data=request.data, partial=True)  # partial=True 允许部分更新
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

# 删除老人
@api_view(['DELETE'])
@permission_classes([IsStaffUserOnly])
def delete_elder(request, pk):
    try:
        elder = Elder.objects.get(pk=pk)
    except Elder.DoesNotExist:
        return Response({'error': '老人信息不存在'}, status=status.HTTP_404_NOT_FOUND)

    try:
        elder.delete()
    except ProtectedError:
        return Response({
            'error': '无法删除该老人，因为存在关联数据（如入住记录、健康档案等）'
        }, status=status.HTTP_400_BAD_REQUEST)

    return Response({'msg': '老人信息删除成功'}, status=status.HTTP_200_OK)
