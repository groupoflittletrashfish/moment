import json

import jwt
from django.http import HttpResponse
from rest_framework.decorators import api_view

from common.config.DatabaseConf import DatabaseSession
from common.pojo.MyJsonResponse import SuccessResponse
from common.utils.commonUtils import get_user
from noname import settings


def hello_world(request):
    # 普通String类型，第二个参数为默认值
    name = request.GET.get('name', '小杂鱼')
    age = request.GET.get('age', 18)
    # 数组/元组等类型的获取
    group = request.GET.getlist('group', [1, 2, 3])
    print(name)
    print(age)
    print(group)
    return HttpResponse('ok')


def post(request):
    # 参数的接收
    data = json.loads(request.body.decode('utf-8'))
    name = data.get('name', 'noname')
    age = data.get('age')
    group = data.get('group')
    # 遍历数组
    print(name)
    print(age)
    for item in group:
        print(item)
    return HttpResponse('ok')


def get_user_info(request):
    token = request.headers.get('token')
    user_info = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    query_sql = """
        SELECT
            m.username,
            m.email,
            s.phone,
            s.nickname,
            s.avatar,
            s.sex,
            s.sign,
            s.netease_cloud_phone,
            s.netease_cloud_password
        FROM
            auth_user m
            LEFT JOIN user_extra s ON m.id = s.user_id 
            AND s.DEL_FLAG = 'N' 
        WHERE
            m.is_active = 1
            AND m.id = '%(user_id)s'
    """
    session = DatabaseSession()
    result = session.read_sql(query_sql, {'user_id': user_info['user_id']})
    result['avatar'] = result['avatar'].apply(lambda x: settings.ftp['url'] + x)
    """
    默认查出来是个数组,那直接转成json数组返回即可，orient='records'的作用是在如果查询一条都没命中，会返回一个全空的对象，所以要解决这个
    result.to_json(orient='records')
    """
    # 但这种情况下明确知道只有一条，所以获取第一条
    row = result.iloc[0]
    return SuccessResponse(row.to_json())


# 绑定网易云音乐
@api_view(['POST'])
def bind_netease_cloud(request):
    user_info = get_user(request)
    params = json.loads(request.body)
    phone = None if params.get('phone') == '' else params.get('phone')
    pwd = None if params.get('password') == '' else params.get('password')
    upt_sql = """
        UPDATE user_extra 
            SET 
            netease_cloud_phone = :phone,
            netease_cloud_password = :password
        WHERE
            user_id = :userId
    """
    session = DatabaseSession().get_session()
    session.execute(upt_sql, {'phone': phone, 'password': pwd, 'userId': user_info['user_id']})
    session.commit()
    return SuccessResponse()
