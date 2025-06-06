from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import OutingRequestSerializer
from .models import OutingRequest
from django.shortcuts import get_object_or_404

# 新增外出申请
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_outing_request(request):
    serializer = OutingRequestSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 查看当前用户的外出申请列表
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_outings(request):
    outings = OutingRequest.objects.filter(user=request.user, is_deleted=False)
    serializer = OutingRequestSerializer(outings, many=True)
    return Response(serializer.data)

# 查看 / 修改 外出申请详情
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def outing_request_detail(request, pk):
    # 获取当前登录用户的未删除外出申请
    outing = get_object_or_404(OutingRequest, pk=pk, user=request.user, is_deleted=False)

    if request.method == 'GET':
        serializer = OutingRequestSerializer(outing)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # 仅允许修改状态为 pending 或 rejected 的申请
        if outing.status not in ['pending', 'rejected']:
            return Response({'detail': f'当前状态为“{outing.status}”，不允许修改'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OutingRequestSerializer(outing, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            # 修改后状态重置为 pending
            serializer.save(status='pending')
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 撤销申请（软删除）
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_outing_request(request, pk):
    # 仅允许撤销状态为 pending 的申请
    outing = get_object_or_404(
        OutingRequest,
        pk=pk,
        user=request.user,
        is_deleted=False,
        status='pending'
    )

    outing.status = 'canceled'
    outing.save()

    return Response({'message': '申请已撤销'}, status=status.HTTP_200_OK)
