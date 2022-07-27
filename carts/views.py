import json

from django.http import JsonResponse
from django.views import View

from carts.models import Cart
from products.models import *
from core.utils import login_decorator

class CartView(View):
    @login_decorator
    def get(self, request):
        cart_list = Cart.objects.select_related('product','user','size','graind')\
                                .prefetch_related('product__productimage_set')\
                                .filter(user=request.user)

        result = [{
            "cart_id"       : cart.id,
            "id"            : cart.product.id,
            "user"          : cart.user.name,
            "product"       : cart.product.name,
            "size"          : cart.size.name,
            "price"         : cart.size.price,
            "graind"        : cart.graind.type,
            "quantity"      : cart.quantity,
            "image"         : cart.product.productimage_set.all()[0].url,
            "is_checked": False
        } for cart in cart_list]

        return JsonResponse({'MESSAGE': result}, status=200)