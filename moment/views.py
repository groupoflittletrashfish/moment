# Create your views here.
import json

from rest_framework.decorators import api_view

from common.config.DatabaseConf import DatabaseSession
from common.models import Moment
from common.pojo.MyJsonResponse import SuccessResponse
from common.utils.commonUtils import get_user, uuid32
from noname import settings


@api_view(['POST'])
def publish(request):
    data = request.data
    # 从token中获取用户信息
    user = get_user(request)
    moment = Moment(ID=uuid32(), moment_desc=data['momentDesc'], moment_media=data['files'],
                    user_id=user['user_id'])
    session = DatabaseSession()
    session.insert(moment)
    return SuccessResponse()


@api_view(['GET'])
def query_all_moment(request):
    query_sql = """
    SELECT
        s.nickname,
        s.avatar,
        m.moment_tag momentTag,
        m.moment_desc momentDesc,
        m.moment_media momentMedia,
        m.moment_position momentPosition
    FROM
        moment m
        LEFT JOIN user_extra s ON m.user_id = s.user_id and s.del_flag = 'N'
    WHERE
        m.del_flag = 'N'
    ORDER BY m.CREATED_TIME DESC
    """
    session = DatabaseSession()
    result = session.read_sql(query_sql)
    if not result.empty:
        result['momentMedia'] = result['momentMedia'].apply(
            lambda x: [settings.ftp['url'] + item for item in json.loads(x)])
        result['avatar'] = result['avatar'].apply(lambda x: settings.ftp['url'] + x)
    return SuccessResponse(result.to_json(orient='records'))
