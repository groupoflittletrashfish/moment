from io import BytesIO

# 文件上传接口
from rest_framework.decorators import api_view

from common.pojo.MyJsonResponse import SuccessResponse
from common.utils.commonUtils import upload_ftp


@api_view(['POST'])
def upload_file(request):
    file = request.FILES['file']
    file_name = file.name
    # 获取文件流
    file_stream = BytesIO(file.read())
    # 上传文件
    upload_ftp(file_stream, file_name)
    return SuccessResponse()
