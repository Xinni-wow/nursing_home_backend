from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

from common.permissions import IsStaffUserOnly
from .models import OutingRequest
from .serializers import OutingRequestSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from django.http import JsonResponse

# 管理员审批接口
@api_view(['GET'])
@permission_classes([IsStaffUserOnly])
def outing_list(request):
    outings = OutingRequest.objects.all()  # 不加 .values()
    serializer = OutingRequestSerializer(outings, many=True)
    return Response(serializer.data)
@api_view(['POST'])
@permission_classes([IsStaffUserOnly])  # 仅管理员可访问
def review_outing_request(request, pk):
    """
    管理员审批外出申请，传入参数：
    - status: 'approved' 或 'rejected'
    - remarks: 备注（可选）
    """
    outing = get_object_or_404(OutingRequest, pk=pk, is_deleted=False)

    if outing.status != 'pending':
        return Response({'detail': '只有待审批状态的申请可以审批'}, status=status.HTTP_400_BAD_REQUEST)

    new_status = request.data.get('status')
    remarks = request.data.get('remarks', '')

    if new_status not in ['approved', 'rejected']:
        return Response({'detail': '无效的审批状态'}, status=status.HTTP_400_BAD_REQUEST)

    outing.status = new_status
    outing.remarks = remarks
    outing.save()

    return Response({'message': '审批成功'}, status=status.HTTP_200_OK)
