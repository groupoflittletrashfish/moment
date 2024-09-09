from django.http import JsonResponse


# 继承JsonResponse，并且确定数据结构
class Response(JsonResponse):
    def __init__(self, code, message, data=None):
        response_data = {
            'code': code,
            'msg': message,
            'data': None
        }
        if data is not None:
            response_data['data'] = data
            # 其实就是调用的JsonResponse的构造函数
        super().__init__(response_data)


# 继承了自定义的Response，也就是上面的类
class SuccessResponse(Response):
    def __init__(self, data=None):
        super().__init__(200, None, data)


# 继承了自定义的Response，也就是上面的类
class FailedResponse(Response):
    def __init__(self, message, code=None):
        if code is None:
            code = 500
        super().__init__(code, message, None)
