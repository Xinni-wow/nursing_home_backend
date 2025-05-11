from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # 定义统一的响应格式
        response.data = {
            'code': response.status_code,
            'message': response.status_text,
            'data': response.data
        }

    return response