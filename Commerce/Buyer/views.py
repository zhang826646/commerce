from django.shortcuts import render,HttpResponseRedirect
from Seller.models import *
from django.http import JsonResponse
import hashlib

def password_md(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return result

def index(request):  #主页
    return render(request,'buyer/index.html',locals())
def login(request):
    error_message = ''
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        if username:
            user=LoginUser.objects.filter(username=username).first()
            if user:
                password=password_md(password)
                db_password=user.password
                if db_password==password:
                    response=HttpResponseRedirect('/Buyer/index/')
                    response.set_cookie('username',user.username)
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

    return render(request,'buyer/login.html',locals())
def register(request):
    error_message=''
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')
        if email:
            user=LoginUser.objects.filter(email=email).first()
            if not user:
                user=LoginUser()
                user.username=username
                user.password=password_md(password)
                user.email=email
                user.save()
            else:
                error_message='邮箱已被注册，请登录'
        else:
            error_message='请填写邮箱'
    else:
        error_message='请求方式有误'

    return render(request,'buyer/register.html',locals())
def logout(request):
    response = HttpResponseRedirect("/Buyer/index/")
    keys = request.COOKIES.keys()
    for key in keys:
        response.delete_cookie(key)
    del request.session["username"]
    return response

def base(request):
    user_id=request.COOKIES.get('user_id')
    cart=Cart.objects.filter(cart_user=int(user_id)).all()
    count=cart.count()
    good_type = GoodsType.objects.all()
    return render(request,'buyer/base.html',locals())
# Create your views here.
def goods_list(request):
    """
    type为请求类型
     k 按照类型查询
        keywords必须为id
     t为关键字查询
        keywords可以是任意关键字
    :param request:
    :return:
    """

    request_type=request.GET.get('type')
    keyword=request.GET.get('keywords')
    goods_list=[]
    if request_type=='t':
        if keyword:
            id=int(keyword)
            goods_type=GoodsType.objects.get(id=id)
            goods_list=goods_type.goods_set.order_by('-goods_pro_time')
    elif request_type=='k':
            if keyword:
                pass
                goods_list=Goods.objects.filter(goods_name__contains=keyword).order_by('-goods_pro_time')
    if goods_list:
        lenth=len(goods_list)/5
        if lenth!=int(lenth):
            lenth+=1
        lenth=int(lenth)
        recommend=goods_list[:lenth]
    return render(request,'buyer/goods_list.html',locals())


def detail(request,id):
    goods= Goods.objects.get(id=int(id))
    return render(request,'buyer/detail.html',locals())

def user_center_info(request):
    return render(request,'buyer/user_center_info.html',locals())

from Buyer.models import *
import time
import datetime
def pay_order(request):
    goods_id = request.GET.get('goods_id')
    count = request.GET.get('count')
    if goods_id and count:
        #保存订单表
        order=PayOrder()
        order.order_number=str(time.time()).replace('.','')
        order.order_data=datetime.datetime.now()
        order.order_status=0
        order.order_user=LoginUser.objects.get(id=int(request.COOKIES.get('user_id')))
        order.save()
        goods=Goods.objects.get(id=int(goods_id))
        order_info=OrderInfo()
        order_info.order_id = order
        order_info.goods_id = goods.id
        order_info.goods_picture = goods.goods_photo
        order_info.goods_name = goods.goods_name
        order_info.goods_count = int(count)
        order_info.goods_price = goods.goods_price
        order_info.goods_total_price = goods.goods_price * int(count)
        order_info.store_id = goods.goods_store  # 商品卖家，goods.goods_store本身就是一条卖家数据
        order_info.save()
        order.order_total = order_info.goods_total_price
        order.save()

    return render(request,'buyer/pay_order.html',locals())

def pay_order_more(request):
    data=request.GET
    data_item=data.items()
    request_data=[]
    for key,value in data_item:
        if key.startswith('check_'):
            goods_id=key.split('_',1)[1]
            count=data.get('count_'+goods_id)
            request_data.append((int(goods_id),int(count)))
    if request_data:
        #保存订单表
        order=PayOrder()
        order.order_number=str(time.time()).replace('.','')
        order.order_data=datetime.datetime.now()
        order.order_status=0
        order.order_user=LoginUser.objects.get(id=int(request.COOKIES.get('user_id')))
        order.save()

        #保存订单详情
        order_total=0
        for goods_id,count in request_data:
            goods=Goods.objects.get(id=int(goods_id))
            order_info=OrderInfo()
            order_info.order_id = order
            order_info.goods_id = goods.id
            order_info.goods_picture = goods.goods_photo
            order_info.goods_name = goods.goods_name
            order_info.goods_count = int(count)
            order_info.goods_price = goods.goods_price
            order_info.goods_total_price = goods.goods_price * int(count)
            order_info.store_id = goods.goods_store  # 商品卖家，goods.goods_store本身就是一条卖家数据
            order_info.save()
            order_total+=order_info.goods_total_price
            order.order_total = order_total   #总价计算
            order.save()

    return render(request,'buyer/pay_order.html',locals())


from alipay import Alipay
from Commerce.settings import alipay_private_key_string,alipay_public_key_string
def AlipayView(request):
    order_number=request.GET.get('order_number')
    order_total=request.GET.get('total')

    # 实例化支付
    alipay = Alipay(
        appid='2016101200667735',
        app_notify_url=None,
        app_private_key_string=alipay_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type='RSA2'
    )
    # 实例化订单
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=str(order_number),
        total_amount=str(order_total),
        subject='服装',
        return_url="/Buyer/pay_result/",
        notify_url="/Buyer/pay_result/",
    )  # 网页支付订单

    # 拼接收款地址=支付宝网关+订单返回参数
    result = "https://openapi.alipaydev.com/gateway.do?" + order_string
    return HttpResponseRedirect(result)

def pay_result(request):
    out_trade_no = request.GET.get("out_trade_no")
    if out_trade_no:
        order = PayOrder.objects.get(order_number=out_trade_no)
        order.order_status = 1
        order.save()
    return render(request,'buyer/pay_result.html')

def add_cart(request):
    result={
        'code':200,
        'data':''
    }
    if request.method=='POST':
        id=int(request.POST.get('goods_id'))
        count=int(request.POST.get('count',1))
        goods=Goods.objects.get(id=id)   #获取id
        cart=Cart()
        cart.goods_name = goods.goods_name
        cart.goods_number = count
        cart.goods_price = goods.goods_price
        cart.goods_picture = goods.goods_photo
        cart.goods_total = goods.goods_price * count
        cart.goods_id = id
        cart.cart_user = request.COOKIES.get("user_id")
        cart.save()
        result['data']='加入购入车成功'
    else:
        result['data']='请求方式错误'
        result['code']=500
    return JsonResponse(result)

def cart(request):
    user_id=request.COOKIES.get('user_id')
    cart=Cart.objects.filter(cart_user=int(user_id)).order_by('-id')
    count=cart.count()
    total=0
    for sta in cart:
        total+=sta.goods_total
    return render(request,'buyer/cart.html',locals())

def user_center_order(request):
    user_id = request.COOKIES.get("user_id")
    user = LoginUser.objects.get(id = int(user_id))
    order_list = user.payorder_set.order_by("-order_data")
    return render(request,"buyer/user_center_order.html",locals())

# Create your views here.
