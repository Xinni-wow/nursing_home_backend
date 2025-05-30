from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from common.permissions import IsStaffUserOnly
from .models import VisitRequest
from .serializers import VisitRequestSerializer
from datetime import datetime, timedelta
import uuid


# 获取所有来访预约
@api_view(['GET'])
@permission_classes([IsStaffUserOnly])
def visit_list(request):
    visits = VisitRequest.objects.filter(is_deleted=False)
    serializer = VisitRequestSerializer(visits, many=True)
    return Response(serializer.data)


# 审批来访预约
@api_view(['POST'])
@permission_classes([IsStaffUserOnly])
def review_visit_request(request, pk):
    visit = get_object_or_404(VisitRequest, pk=pk, is_deleted=False)

    if visit.status != 'pending':
        return Response(
            {'detail': '只有待审批状态的预约可以审批'},
            status=status.HTTP_400_BAD_REQUEST
        )

    new_status = request.data.get('status')
    remarks = request.data.get('remarks', '')

    if new_status not in ['approved', 'rejected']:
        return Response(
            {'detail': '无效的审批状态'},
            status=status.HTTP_400_BAD_REQUEST
        )

    visit.status = new_status
    visit.remarks = remarks

    # 如果审批通过，生成二维码
    if new_status == 'approved':
        visit.qr_code = f"VISIT-{uuid.uuid4().hex[:8]}"
        visit.qr_code_expiry = datetime.now() + timedelta(days=1)

    visit.save()

    return Response(
        {'message': '审批成功', 'qr_code': visit.qr_code if new_status == 'approved' else None},
        status=status.HTTP_200_OK
    )