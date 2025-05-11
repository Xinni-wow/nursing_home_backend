from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # 定义统一的响应格式
        unified_response = {
            'code': renderer_context['response'].status_code,
            'message': renderer_context['response'].status_text,
            'data': data
        }

        return super().render(unified_response, accepted_media_type, renderer_context)
