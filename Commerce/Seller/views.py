from django.shortcuts import render,HttpResponseRedirect
from Seller.models import *
from django.http import JsonResponse

import hashlib

def password_md(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return result

def loginValid(fun):
    def inner(request,*args,**kwargs):
        cookie_username=request.COOKIES.get('username')
        session_username=request.session.get('username')
        if cookie_username and session_username and cookie_username==session_username:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/Seller/login/')
    return inner


def index(request):  #主页
    return render(request,'seller/index.html',locals())

import datetime
import time
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def login(request):
    error_message = ''
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        if email:
            user=LoginUser.objects.filter(email=email).first()
            if user:
                password=password_md(password)
                db_password=user.password
                code = request.POST.get('valid_code')
                if password == db_password:
                    # 获取验证码
                    codes = Valid_Code.objects.filter(code_user=email).order_by('-code_time').first()
                    # now = time.mktime(datetime.datetime.now().timetuple())
                    # db_time = time.mktime(codes.code_time.timetuple())
                    # t = (now - db_time) / 60
                    # if codes and codes.code_state == 0 and t <= 5
                    if codes.code_content.upper() == code.upper():
                        response = HttpResponseRedirect('/Seller/index/')
                        response.set_cookie('username', user.username)
                        response.set_cookie('user_id', user.id)
                        request.session['username'] = user.username
                        return response
                    else:
                        error_message = '验证码不正确'
                else:
                    error_message='密码有误'
            else:
                error_message='用户不存在'
        else:
            error_message='请输入用户名'
    else:
        error_message='请求方式有误'

    return render(request,'seller/login.html',locals())



def register(request):
    error_message=''
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        email=request.POST.get('email')
        if email:
            user=LoginUser.objects.filter(email=email).first()
            if not user:
                user=LoginUser()
                user.username=email
                user.password=password_md(password)
                user.email=email
                user.user_type=1
                user.save()
            else:
                error_message='邮箱已被注册，请登录'
        else:
            error_message='请填写邮箱'
    else:
        error_message='请求方式有误'

    return render(request,'seller/register.html',locals())

import json
import requests
from Commerce.settings import DING_URL
def sendDing(content,to=None):
    headers = {
        "Content-Type": "application/json",
        "Charset": "utf-8"
    }
    requests_data = {
        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {
            "atMobiles": [
            ],
            "isAtAll": True
        }
    }
    if to:
        requests_data["at"]["atMobiles"].append(to)
        requests_data["at"]["isAtAll"] = False
    else:
        requests_data["at"]["atMobiles"].clear()
        requests_data["at"]["isAtAll"] = True
    sendData = json.dumps(requests_data)
    response = requests.post(url=DING_URL, headers=headers, data=sendData)
    content = response.json()
    return content

import random
def random_code(len=6):
    """
    生成6位验证码
    """
    string = "1234567890"
    valid_code = "".join([random.choice(string) for i in range(len)])
    return valid_code


from CeleryTask.tasks import sendDing
@csrf_exempt
def send_login_code(request):
    result = {
        "code": 200,
        "data": ""
    }
    if request.method == "POST":
        email = request.POST.get("email")
        code = random_code()
        c = Valid_Code()
        c.code_user = email
        c.code_content = code
        c.save()
        send_data = "%s的验证码是%s,打死也不要告诉别人哟"%(email,code)
        sendDing.delay(send_data)
        #sendDing(send_data) #发送验证
        result["data"] = "发送成功"
    else:
        result["code"] = 400
        result["data"] = "请求错误"
    return JsonResponse(result)

from django.core.paginator import Paginator
from django.shortcuts import render_to_response
def newList(request):
    p = 1
    page_size = 6
    articles = Goods.objects.order_by("-public_time")
    article_list = Paginator(articles,page_size) #进行分页
    page_article= article_list.page(p)
    return render_to_response("newlist.html",locals())