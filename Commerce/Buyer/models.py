from django.db import models

from Seller.models import *

class PayOrder(models.Model):
    """
    订单表
    订单状态
    0 未支付
    1 已支付
    2 待发货
    3 待收货
    4/5 完成/拒收
    """
    order_number=models.CharField(max_length=32)    #订单编号
    order_data=models.DateTimeField(auto_now=True)   #订单时间
    # order_status=models.IntegerField()              #订单状态
    order_total=models.FloatField(blank=True,null=True)   #订单总价
    order_user=models.ForeignKey(to=LoginUser,on_delete=models.CASCADE)   #订单买家

class OrderInfo(models.Model):
    """
    订单详情表
    """
    order_id=models.ForeignKey(to=PayOrder,on_delete=models.CASCADE)  #对应订单表id
    goods_id=models.IntegerField()                   #订单id
    goods_picture = models.CharField(max_length=32)  #订单商品照片
    goods_name = models.CharField(max_length=32)     #订单商品名称
    goods_count = models.IntegerField()              #订单商品数量
    goods_price = models.FloatField()                #订单商品单钱
    goods_total_price = models.FloatField()    #订单商品总价
    order_status=models.IntegerField(default=0)
    store_id = models.ForeignKey(to=LoginUser,on_delete=models.CASCADE)  #商品对应商家


class Cart(models.Model):
    """
    购物车：
    商品id
    商品名称
    商品数量
    商品价格
    商品总价
    用户
    """
    goods_name=models.CharField(max_length=32)
    goods_number=models.IntegerField()
    goods_price=models.FloatField()
    goods_picture=models.CharField(max_length=32)
    goods_total=models.FloatField()
    goods_id=models.IntegerField()
    cart_user=models.IntegerField()
# Create your models here.

# Create your models here.
