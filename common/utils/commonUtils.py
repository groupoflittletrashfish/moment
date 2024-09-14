import ftplib
import uuid
from datetime import datetime

import jwt

from noname import settings


def get_user(request):
    token = request.headers.get('token')
    return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])


def uuid32():
    random_uuid = uuid.uuid4()
    return str(random_uuid).replace('-', '')


# 上传文件到ftp
def upload_ftp(file_stream, file_name, user_id):
    try:
        config = settings.ftp
        with ftplib.FTP() as ftp:
            ftp.connect(config['host'], config['port'])
            ftp.login(config['user'], config['password'])
            # ftp主动连接方式，ftp有两种连接形式，自行查阅资料
            ftp.set_pasv(False)

            # 获取用户信息，创建专属文件夹
            path = f"{config['path']}/{user_id}/{datetime.today().date()}"
            directories = path.split('/')
            for dir_part in directories:
                if dir_part:
                    try:
                        ftp.cwd(dir_part)  # 尝试切换到该目录
                    except ftplib.error_perm:  # 如果目录不存在
                        ftp.mkd(dir_part)  # 创建目录
                        ftp.cwd(dir_part)  # 切换到新创建的目录
                # 上传文件流
            ftp.storbinary(f'STOR {file_name}', file_stream)
            return f'{path}/{file_name}'
    except Exception as e:
        print(f'happen an error:{e}')
    return None
