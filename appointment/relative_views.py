from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import VisitRequest
from .serializers import VisitRequestSerializer
import qrcode
from io import BytesIO
from django.http import HttpResponse
from .models import VisitRequest
from django.views.decorators.csrf import csrf_exempt

# 新增来访预约
@api_view(['POST'])
@permission_classes([AllowAny])
def add_visit_request(request):
    serializer = VisitRequestSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 获取用户来访预约列表
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_visits(request):
    visits = VisitRequest.objects.filter(user=request.user, is_deleted=False)
    serializer = VisitRequestSerializer(visits, many=True)
    return Response(serializer.data)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import VisitRequest
from .serializers import VisitRequestSerializer

@api_view(['GET', 'PUT'])
def visit_detail(request, pk):
    try:
        visit = VisitRequest.objects.get(pk=pk)
    except VisitRequest.DoesNotExist:
        return Response({'detail': '预约不存在'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VisitRequestSerializer(visit)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = VisitRequestSerializer(visit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 获取来访预约详情
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def visit_request_detail(request, pk):
    visit = get_object_or_404(VisitRequest, pk=pk, user=request.user, is_deleted=False)
    serializer = VisitRequestSerializer(visit)
    return Response(serializer.data)


# 取消来访预约
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_visit_request(request, pk):
    visit = get_object_or_404(
        VisitRequest,
        pk=pk,
        user=request.user,
        is_deleted=False,
        status='pending'
    )
    visit.status = 'canceled'
    visit.save()
    return Response({'message': '来访预约已取消'}, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 如果你能保证请求是安全的
def get_visit_qrcode(request, pk):
    visit = get_object_or_404(VisitRequest, pk=pk, is_deleted=False)

    if visit.status != 'approved' or not visit.qr_code:
        return Response({'detail': '无效的二维码请求'}, status=status.HTTP_400_BAD_REQUEST)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(visit.qr_code)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")

    response = HttpResponse(buffer.getvalue(), content_type="image/png")
    response['Content-Disposition'] = 'inline; filename="qrcode.png"'
    return response