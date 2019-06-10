"""iot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from iot.views import *
urlpatterns = [
    url('^admin/$', admin.site.urls),
    url('^$',view_user,name='user'),
    url('^login/$',view_login,name='login'),
    url('^logout/$',view_logout,name='logout'),
    url('^regist/$',view_regist,name='regist'),
    url('^vc/$',view_verifycode,name='verifycode'),
    url('^ssba/$',view_starry_sky_box_api,name='starry_sky_box_api'),
    url('^sa/$',view_switch_device_api,name='switch_device_api'),
    url('^di/$',view_devices_info,name='devices_info')
]
