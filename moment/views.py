# Create your views here.
import json

from rest_framework.decorators import api_view

from common.config import DatabaseConf
from common.config.DatabaseConf import DatabaseSession
from common.models import Moment, MomentTag
from common.pojo.MyJsonResponse import SuccessResponse
from common.utils.commonUtils import get_user, uuid32
from noname import settings


@api_view(['POST'])
def publish(request):
    data = request.data
    # 从token中获取用户信息
    user = get_user(request)
    moment = Moment(ID=uuid32(), moment_desc=data['momentDesc'], moment_media=data['files'],
                    user_id=user['user_id'], moment_tag=data['tags'])
    session = DatabaseSession()
    session.insert(moment)
    return SuccessResponse()


@api_view(['GET'])
def query_all_moment(request):
    index = request.query_params.get('index', 1)
    offset = request.query_params.get('offset', 2)
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
    limit %(page)s, %(offset)s
    """
    session = DatabaseSession()
    page_info = DatabaseSession.page(index, offset)
    result = session.read_sql(query_sql, {'page': page_info['page'], 'offset': page_info['offset']})
    if not result.empty:
        result['momentMedia'] = result['momentMedia'].apply(
            lambda x: [settings.ftp['url'] + item for item in json.loads(x)])
        result['avatar'] = result['avatar'].apply(lambda x: settings.ftp['url'] + x)
    return SuccessResponse(result.to_json(orient='records'))


@api_view(['GET'])
def query_all_tags(request):
    query_sql = """
        select ID,tag_desc from moment_tags where DEL_FLAG = 'N' limit 100
    """
    session = DatabaseSession()
    result = session.read_sql(query_sql)
    return SuccessResponse(result.to_json(orient='records'))


@api_view(['POST'])
def addTag(request):
    params = json.loads(request.body.decode('utf-8'))
    query_sql = """
        select count(1) cn from moment_tags where DEL_FLAG = 'N' and tag_desc = %(desc)s
    """
    session = DatabaseSession()
    result = session.read_sql(query_sql, {'desc': params['desc']})
    row = result.iloc[0]
    if row['cn'] > 0:
        return SuccessResponse()
    else:
        tag = MomentTag(ID=uuid32(), tag_desc=params['desc'])
        session.insert(tag)
    return SuccessResponse()
