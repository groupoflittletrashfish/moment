# Create your views here.
from rest_framework.decorators import api_view

from common.config.DatabaseConf import DatabaseSession
from common.models import Moment
from common.pojo.MyJsonResponse import SuccessResponse
from common.utils.commonUtils import get_user, uuid32


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
    query_sql = "select * from moment where del_flag = %(delFlag)s"
    session = DatabaseSession()
    result = session.read_sql(query_sql, params={'delFlag': 'N'})
    return SuccessResponse(result)
