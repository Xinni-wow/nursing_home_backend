from django.utils import timezone
import random
from .models import Room, CheckIn, Bill
from .serializers import RoomSerializer, CheckInSerializer, ElderSerializer, BillSerializer
from elders.models import Elder
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import calculate_fee_by_years
from alipay import AliPay
from django.conf import settings
import csv
from django.http import HttpResponse
from .models import Bill
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models.functions import TruncDay
from django.db.models import Sum, Count


# 用户专用接口 - 简单直接，不分页
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_checkins(request):
    """用户查看自己的入住记录"""
    checkins = CheckIn.objects.filter(elder__user=request.user)
    serializer = CheckInSerializer(checkins, many=True)
    return Response(serializer.data)


# 管理员专用接口 - 保持现有的分页和搜索功能
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_admin_checkins(request):
    """管理员查看所有入住记录（带分页和搜索）"""
    if request.user.user_type != 'staff':
        return Response({'error': '无权限'}, status=403)

    checkins = CheckIn.objects.all()

    # 搜索功能
    elder_name = request.GET.get('elder')
    room_number = request.GET.get('room')
    status_param = request.GET.get('status')

    if elder_name:
        checkins = checkins.filter(elder__full_name__icontains=elder_name)
    if room_number:
        checkins = checkins.filter(room__room_number__icontains=room_number)
    if status_param:
        checkins = checkins.filter(status=status_param)

    # 分页
    paginator = PageNumberPagination()
    paginator.page_size_query_param = 'page_size'
    result_page = paginator.paginate_queryset(checkins, request)
    serializer = CheckInSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_bills_csv(request):
    if request.user.user_type != 'staff':
        return HttpResponse("无权限", status=403)

    elder_name = request.GET.get('elder_name')
    room_number = request.GET.get('room_number')
    bill_type = request.GET.get('type')

    bills = Bill.objects.all()
    print("请求参数 elder_name:", elder_name)
    print("请求参数 room_number:", room_number)
    print("请求参数 bill_type:", bill_type)
    print("筛选前账单数量:", bills.count())

    if elder_name:
        bills = bills.filter(elder__full_name__icontains=elder_name)
    if room_number:
        bills = bills.filter(checkin__room__room_number__icontains=room_number)
    if bill_type:
        bills = bills.filter(type=bill_type)

    print("筛选后账单数量:", bills.count())
    for bill in bills:
        print(f"导出账单 - 姓名: {bill.elder.full_name}, 房间: {bill.checkin.room.room_number}, 类型: {bill.type}")

    # 创建 CSV 响应
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="bills_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['老人姓名', '房间号', '账单类型', '住宿费', '餐饮费', '总费用', '支付时间'])

    for bill in bills:
        writer.writerow([
            bill.elder.full_name,
            bill.checkin.room.room_number,
            '初次入住' if bill.type == 'initial' else '续费',
            bill.stay_fee,
            bill.meal_fee,
            bill.total_fee,
            bill.created_at.strftime('%Y-%m-%d %H:%M')
        ])

    return response

@api_view(['POST'])
def checkout_elder(request, checkin_id):
    try:
        checkin = CheckIn.objects.get(id=checkin_id)
        if checkin.status == 'left':
            return Response({"message": "该老人已退房"}, status=status.HTTP_400_BAD_REQUEST)
        checkin.status = 'left'
        checkin.save()
        if not CheckIn.objects.filter(room=checkin.room, status='active').exists():
            checkin.room.is_occupied = False
            checkin.room.save()
        return Response({"message": "退房成功"}, status=200)
    except CheckIn.DoesNotExist:
        return Response({"error": "入住记录不存在"}, status=404)

@api_view(['POST'])
def generate_pay_url(request):
    print("进入了支付函数")
    data = request.data
    elder = data.get('elder')
    room = data.get('room')
    start_date = data.get('start_date')
    duration = int(data.get('duration_years', 1))
    pay_type = data.get('type', 'checkin')  # 默认是入住

    # 生成唯一订单号
    out_trade_no = f"{timezone.now().strftime('%Y%m%d%H%M%S')}{random.randint(1000, 9999)}"

    # 费用计算
    fees = calculate_fee_by_years(duration)
    total_amount = str(fees['total_fee'])

    alipay = get_alipay_client()
    # 构造携带参数的 return_url，包含 start_date
    return_url = (
        f"{settings.ALIPAY_CONFIG['RETURN_URL']}"
        f"?elder={elder}&room={room}&duration_years={duration}&start_date={start_date}&type={pay_type}"
    )

    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=out_trade_no,
        total_amount=total_amount,
        subject=f"护理院支付 - 老人ID:{elder}",
        return_url=return_url,
        notify_url=settings.ALIPAY_CONFIG['NOTIFY_URL']
    )

    pay_url = f"{settings.ALIPAY_CONFIG['GATEWAY']}?{order_string}"
    print("支付宝支付跳转地址：", pay_url)
    return Response({
        "pay_url": pay_url,
        "order_id": out_trade_no
    }
    )

class MyElders(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        elders = Elder.objects.filter(user=request.user)
        serializer = ElderSerializer(elders, many=True)
        return Response(serializer.data)

class AvailableRoomList(APIView):
    def get(self, request):
        rooms = Room.objects.filter(is_occupied=False)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SubmitCheckIn(APIView):
    def post(self, request):
        # 删除非模型字段，避免错误
        checkin_data = request.data.copy()
        checkin_data.pop('stay_fee', None)
        checkin_data.pop('meal_fee', None)
        checkin_data.pop('total_fee', None)

        serializer = CheckInSerializer(data=checkin_data)
        if serializer.is_valid():
            checkin = serializer.save()
            years = checkin.duration_years
            fees = calculate_fee_by_years(years)
            Bill.objects.create(
                checkin=checkin,
                elder=checkin.elder,
                years=years,
                stay_fee=fees['stay_fee'],
                meal_fee=fees['meal_fee'],
                total_fee=fees['total_fee'],
                type='initial'
            )
            return Response({
                'message': '入住成功',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def calculate_fee(request):
    years = int(request.data.get('duration_years', 1))
    fees = calculate_fee_by_years(years)
    return Response(fees)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def renew_checkin(request):
    data = request.data
    elder_id = data.get('elder')

    try:
        checkin = CheckIn.objects.get(elder=elder_id, status='active')
    except CheckIn.DoesNotExist:
        return Response({"error": "找不到该老人的在住记录"}, status=400)

    # 解析续费年限
    years = int(data.get('duration_years', 1))

    # 更新入住年限
    checkin.duration_years += years
    checkin.save()

    # 计算费用
    fees = calculate_fee_by_years(years)

    # 生成新账单
    Bill.objects.create(
        checkin=checkin,
        elder=checkin.elder,
        years=years,
        stay_fee=fees['stay_fee'],
        meal_fee=fees['meal_fee'],
        total_fee=fees['total_fee'],
        type='renew'
    )

    return Response({
        "message": "续费成功",
        "total_fee": fees['total_fee']
    }, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_bills(request):
    user = request.user
    bills = Bill.objects.filter(elder__user=user).order_by('-created_at')
    serializer = BillSerializer(bills, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_bills(request):
    if request.user.user_type != 'staff':
        return Response({'error': '无权限'}, status=403)

    bills = Bill.objects.all().order_by('-created_at')

    # 使用统一的参数名
    elder_name = request.GET.get('elder', '')
    room_number = request.GET.get('room', '')
    bill_type = request.GET.get('type', '')

    if elder_name:
        bills = bills.filter(elder__full_name__icontains=elder_name)
    if room_number:
        bills = bills.filter(checkin__room__room_number__icontains=room_number)
    if bill_type:
        bills = bills.filter(type=bill_type)

    # 如果需要分页
    page = request.GET.get('page')
    if page:
        paginator = PageNumberPagination()
        paginator.page_size_query_param = 'page_size'
        result_page = paginator.paginate_queryset(bills, request)
        serializer = BillSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    else:
        # 不分页直接返回
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data)

def get_alipay_client():
    return AliPay(
        appid=settings.ALIPAY_CONFIG['APP_ID'],
        app_notify_url=settings.ALIPAY_CONFIG['NOTIFY_URL'],
        app_private_key_string=open(settings.ALIPAY_CONFIG['APP_PRIVATE_KEY_PATH']).read(),
        alipay_public_key_string=open(settings.ALIPAY_CONFIG['ALIPAY_PUBLIC_KEY_PATH']).read(),
        sign_type="RSA2",
        debug=True  # 沙箱环境
    )
