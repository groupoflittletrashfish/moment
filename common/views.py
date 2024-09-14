from io import BytesIO

# 文件上传接口
import jwt
from rest_framework.decorators import api_view

from common.pojo.MyJsonResponse import SuccessResponse, FailedResponse
from common.utils.commonUtils import upload_ftp
from noname import settings


@api_view(['POST'])
def upload_file(request):
    file = request.FILES['file']
    file_name = file.name
    # 获取文件流
    file_stream = BytesIO(file.read())
    # 上传文件
    token = request.headers.get('token')
    user_info = None
    try:
        user_info = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        # 输出结果如下：{'user_id': 17, 'username': 'noname', 'email': '', 'exp': 1724921614}
    except Exception:
        return FailedResponse(code=401, message='鉴权失败')
    path = upload_ftp(file_stream, file_name, user_info['user_id'])
    return SuccessResponse(path)
