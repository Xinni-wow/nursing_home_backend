# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import date, timedelta
from .models import DailyMenu
from .serializers import DailyMenuSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_menu_view(request):
    today = date.today()
    end_date = today + timedelta(days=13)
    query_date = request.query_params.get('date')

    if query_date:
        queryset = DailyMenu.objects.filter(date=query_date)
    else:
        queryset = DailyMenu.objects.filter(date__gte=today, date__lte=end_date)

    serializer = DailyMenuSerializer(queryset, many=True)
    return Response(serializer.data)

