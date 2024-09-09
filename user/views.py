import json

from django.http import HttpResponse


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
