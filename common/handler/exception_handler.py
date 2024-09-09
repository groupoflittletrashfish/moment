import json
import traceback

from django.utils.deprecation import MiddlewareMixin

from common.pojo.MyJsonResponse import FailedResponse


# 继承MiddlewareMixin，重写process_exception
class ExceptionMiddleware(MiddlewareMixin):
    @staticmethod
    def process_exception(request, exception):
        # 如果错误类型是ZeroDivisionError，则XXXX
        if isinstance(exception, ZeroDivisionError):
            # 返回统一错误对象
            return FailedResponse(exception.args[0])
        else:
            traceback.print_exc()
            return FailedResponse(exception.args[0])
