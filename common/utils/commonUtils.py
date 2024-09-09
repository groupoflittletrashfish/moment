import ftplib
import uuid

import jwt

from noname import settings


def get_user(request):
    token = request.headers.get('token')
    return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])


def uuid32():
    random_uuid = uuid.uuid4()
    return str(random_uuid).replace('-', '')


# 上传文件到ftp
def upload_ftp(file_stream, file_name):
    try:
        config = settings.ftp
        with ftplib.FTP() as ftp:
            ftp.connect(config['host'], config['port'])
            ftp.login(config['user'], config['password'])
            # ftp主动连接方式，ftp有两种连接形式，自行查阅资料
            ftp.set_pasv(False)
            # 上传文件流
            ftp.storbinary(f'STOR {file_name}', file_stream)
    except Exception as e:
        print(f'happen an error:{e}')
    return True
