from django.shortcuts import render,HttpResponseRedirect
from Seller.models import *
import hashlib

def password_md(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return result

def index(request):  #主页
    return render(request,'seller/index.html',locals())
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
                if db_password==password:
                    response=HttpResponseRedirect('/Seller/index/')
                    response.set_cookie('email',user.email)
                    response.set_cookie('user_id',user.id)
                    request.session['username']=user.username
                    return response
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
# Create your views here.

# Create your views here.
