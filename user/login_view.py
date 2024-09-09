import datetime
import json

import jwt
from django.contrib.auth import authenticate

from common.pojo.MyJsonResponse import SuccessResponse
from noname import settings


def login(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    print(user)
    if user is None:
        raise RuntimeError('用户名密码错误')

    # 使用pyjwt生成jwt
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    # 可以放入一些自定义的参数
    payload = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'exp': expiration
    }
    # settings.SECRET_KEY是配置在settings.py里的密钥
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return SuccessResponse(token)
