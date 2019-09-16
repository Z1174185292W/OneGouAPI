# 购物车信息
from datetime import datetime

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from CartList.models import OrderGoods
from .api import Order_list_1_SeraLier, Order_listModel, CartModel
from Goods.api import GoodsModel, GoodsModel_twoSerializers, GoodsInfoModel, GoodsImage_OneSerializers, GoodsImageModel
from Address.models import AddressModel


class GetCartView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        goods = request.POST.get('goods_id')
        users = request.session.get('user')

        order_id = Order_listModel.objects.filter(order_id__user_id=users).first()
        count = Order_list_1_SeraLier(instance=order_id).data

        goods_info = GoodsModel.objects.filter(id=users).first()
        goods_data = GoodsModel_twoSerializers(instance=goods_info).data

        return JsonResponse({
            "cart_datas": [
                {
                    "goods_id": goods,
                    "goods_num": count,
                    "user_id": users,
                    "goods_detail": goods_data
                }
            ]
        })


class AddCartView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        goods_id = request.POST.get('goods_id')
        user_id = request.session.get('user')

        # 判断用户是否有购物车
        user_cart = CartModel.objects.filter(user_id=user_id).all()
        address = AddressModel.objects.get(Q(user=user_id) & Q(state=True))
        address_id = address.id

        if not user_cart:
            CartModel(user_id=user_id).save()
        else:
            add = request.POST.get('add_goods')
            sub = request.POST.get('sub_goods')
            card_id = CartModel.objects.get(user_id=user_id)
            if add:
                order_list = Order_listModel.objects.filter(Q(order_id__card_id=card_id) & Q(goods_id=goods_id)).first()
                if order_list:
                    order_list_1 = OrderGoods()
                    order_list_count = order_list_1.count + 1
                    Order_listModel(count=order_list_count).save()
                else:
                    order = Order_listModel(user_id=user_id, card_id=card_id)
                    order_id = order.id

                    start_time = str(datetime.now())
                    order_statud = 0
                    goods_id = goods_id
                    count = 1
                    addr_id = address_id
                    Order_listModel(order_id=order_id, start_time=start_time, order_statud=order_statud,
                                    goods_id=goods_id, count=count, addr_id=addr_id).save()
            if sub:
                order_list = Order_listModel.objects.filter(Q(order_id__card_id=card_id) & Q(goods_id=goods_id)).first()
                if order_list:
                    order_list_1 = OrderGoods()
                    order_list_count = order_list_1.count - 1
                    Order_listModel(count=order_list_count).save()


class OrderDownView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        # 获取商品的数量
        order_num = request.POST.get('order_num')

        # 获取商品的优惠价以及总价
        goods_id = request.POST.get('goods_id')
        goods = GoodsInfoModel.objects.get(goods_id=goods_id)
        goods_price = goods.sellprice
        price = goods_price * int(order_num)

        # 获取地址
        # 如果用户填写地址以及手机号和姓名等信息
        address = request.POST.get('address', None)
        phone = request.POST.get('phone', None)
        name = request.POST.get('name', None)

        # 获取商品的名字
        goods_name = goods.goods_id.commodityname

        # 获取商品的图片
        goods_img = GoodsImageModel.objects.filter(goods_id=goods_id).all()
        goods_img_serializer = GoodsImage_OneSerializers(instance=goods_img, many=True)

        return JsonResponse({
            "code": 200,
            "order_num": order_num,
            "total_price": price,
            "addr": {
                "phone": phone,
                "name": name,
                "address": address
            },
            "goods": [
                {
                    "img": goods_img_serializer.data,
                    "price": goods_price,
                    "cnt": order_num
                }
            ]
        })


