"""Commerce URL Configuration

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
from django.urls import path,re_path
from Buyer.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index),
    path('login/', login),
    path('register/', register),
    path('logout/', logout),
    path('base/', base),
    path('goods_list/', goods_list),
    re_path(r'detail/(?P<id>\d{1,2})/', detail),
    path('user_info/', user_center_info),
    path('pay_order/', pay_order),
    path('pay_order_more/', pay_order_more),
    path('alipay/', AlipayView),
    path('pay_result/', pay_result),
    path('add_cart/', add_cart),
    path('cart/', cart),
    path('user_center_order/', user_center_order)
]