from django.urls import path
from.views import (
    AvailableRoomList,
    SubmitCheckIn,
    calculate_fee,
    MyElders,
    get_user_checkins,
    get_admin_checkins,
    checkout_elder,
    renew_checkin,
    get_my_bills,
    get_all_bills,
    export_bills_csv,
    generate_pay_url
)
urlpatterns = [
    path('rooms/available/', AvailableRoomList.as_view()),
    path('checkin/', SubmitCheckIn.as_view()),
    path('calculate_fee/', calculate_fee),
    path('elders/', MyElders.as_view()),
    path('generate_pay_url/',generate_pay_url),
    path('checkout/<int:checkin_id>/', checkout_elder),
    path('checkins/user/', get_user_checkins, name='user-checkins'),  # 查询入住记录（无分页）
    path('bills/', get_my_bills, name='user-bills'),  # 用户查自己账单（无分页）
    path('bills/all/', get_all_bills),  # 管理员查全部账单
    path('checkin/renew/', renew_checkin, name='renew-checkin'),
    path('bills/export/', export_bills_csv, name='export-bills'),
    path('checkins/admin/', get_admin_checkins, name='get-checkins'),
]

