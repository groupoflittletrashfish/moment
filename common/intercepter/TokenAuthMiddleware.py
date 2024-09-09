import jwt

from common.pojo.MyJsonResponse import FailedResponse
from noname import settings


class TokenAuthMiddleware:
    # 构造器，get_response代表的是获取下一个中间件
    def __init__(self, get_response):
        self.get_response = get_response
        # 不验证的接口
        self.exclude = ['/login', '/admin/', '/admin/login/']

    # call函数是中间件处理请求的时候会被调用
    def __call__(self, request):
        # 如果地址不验证的接口，则直接放行，调用下一个中间件
        if request.path in self.exclude:
            return self.get_response(request)

        token = request.headers.get('token')
        if not token:
            return FailedResponse(code=401, message='未登录')
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # 输出结果如下：{'user_id': 17, 'username': 'noname', 'email': '', 'exp': 1724921614}
        except Exception:
            return FailedResponse(code=401, message='鉴权失败')

        return self.get_response(request)
