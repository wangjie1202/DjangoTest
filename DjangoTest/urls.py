"""DjangoTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from MyAppTest import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('bigApp_ApiList/', views.bigApp_ApiList),
    path('bigApp_getBasicInfo/', views.bigApp_getBasicInfo),
    path('bigApp_login/', views.bigApp_login),
    path('bigApp_feedBack/', views.bigApp_feedBack),
    path('bigApp_getCode/', views.bigApp_getCode),
    path('lilly_ApiList/', views.lilly_ApiList),
    path('lilly_login/', views.lilly_login),
    path('lilly_getOneTemp/', views.lilly_getOneTemp),
    path('lenglian_ApiList/', views.lenglian_ApiList),
    path('lenglian_login/', views.lenglian_login),
]
