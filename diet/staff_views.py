from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import date, timedelta
from .models import DailyMenu
from .serializers import DailyMenuSerializer
from common.permissions import IsStaffUserOnly

@api_view(['POST'])
@permission_classes([IsStaffUserOnly])
def menu_manage(request):
    try:
        # 手动提取字段，跳过 DRF 的唯一性验证
        raw_data = request.data
        date_val = raw_data['date']
        meal_type = raw_data['meal_type']
        content = raw_data['content']
    except KeyError:
        return Response({'detail': '参数缺失'}, status=400)

    # 限制日期范围
    today = date.today()
    target_date = date.fromisoformat(date_val)
    if not (today <= target_date <= today + timedelta(weeks=4)):
        return Response({'detail': '只能添加或修改本周及未来 4 周的菜单'}, status=400)

    obj, created = DailyMenu.objects.update_or_create(
        date=target_date,
        meal_type=meal_type,
        defaults={
            'content': content,
            'modified_by': request.user
        }
    )

    result_serializer = DailyMenuSerializer(obj)
    return Response(result_serializer.data, status=201 if created else 200)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import date, timedelta
from .models import DailyMenu
from .serializers import DailyMenuSerializer
from common.permissions import IsStaffUserOnly

@api_view(['POST'])
@permission_classes([IsStaffUserOnly])
def menu_manage(request):
    try:
        # 手动提取字段，跳过 DRF 的唯一性验证
        raw_data = request.data
        date_val = raw_data['date']
        meal_type = raw_data['meal_type']
        content = raw_data['content']
    except KeyError:
        return Response({'detail': '参数缺失'}, status=400)

    # 限制日期范围
    today = date.today()
    target_date = date.fromisoformat(date_val)
    if not (today <= target_date <= today + timedelta(weeks=4)):
        return Response({'detail': '只能添加或修改本周及未来 4 周的菜单'}, status=400)

    obj, created = DailyMenu.objects.update_or_create(
        date=target_date,
        meal_type=meal_type,
        defaults={
            'content': content,
            'modified_by': request.user
        }
    )

    result_serializer = DailyMenuSerializer(obj)
    return Response(result_serializer.data, status=201 if created else 200)

@api_view(['GET'])
@permission_classes([IsStaffUserOnly])
def menu_list(request):
    """
    支持查询参数：
    - start_date: 开始日期（可选，默认今天）
    - end_date: 结束日期（可选，默认今天 + 4 周）
    """
    today = date.today()
    start_date_str = request.query_params.get('start_date')
    end_date_str = request.query_params.get('end_date')

    try:
        start_date = date.fromisoformat(start_date_str) if start_date_str else today
        end_date = date.fromisoformat(end_date_str) if end_date_str else today + timedelta(weeks=4)
    except ValueError:
        return Response({'detail': '日期格式错误，应为 YYYY-MM-DD'}, status=400)

    if start_date > end_date:
        return Response({'detail': '开始日期不能晚于结束日期'}, status=400)

    menus = DailyMenu.objects.filter(date__range=(start_date, end_date)).order_by('date', 'meal_type')
    serializer = DailyMenuSerializer(menus, many=True)
    return Response(serializer.data)
