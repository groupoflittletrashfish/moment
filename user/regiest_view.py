import json

from django.contrib.auth.models import User

from common.pojo.MyJsonResponse import Response, SuccessResponse


def regiest(request):
    # 前端传入的参数
    data = json.loads(request.body)
    username = data.get('username')
    pwd1 = data.get('password1')
    pwd2 = data.get('password2')
    if pwd1 != pwd2:
        raise RuntimeError('两次密码输入不一致')
    user = User.objects.create_user(username=username, password=pwd1)
    # django返回的user无法被json序列化，所以需要自己重新定义一个返回对象，如果有需要的话
    rt_data = {
        "username": username
    }
    return SuccessResponse()
