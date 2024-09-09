"""
URL configuration for noname project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import user.login_view
import user.regiest_view
import user.views
from common.views import upload_file
from moment.views import publish, query_all_moment

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello', user.views.hello_world),
    path('post', user.views.post),
    path('login', user.login_view.login),
    path('regiest', user.regiest_view.regiest),
    path('upload', upload_file),
    path('moment/publish', publish),
    path('moment/queryAllMoment', query_all_moment),
]
