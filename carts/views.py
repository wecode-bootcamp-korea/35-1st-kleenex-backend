import json

from django.http import JsonResponse
from django.views import View

from carts.models import Cart
from products.models import *
from core.utils import login_decorator

class CartView(View):
    @login_decorator
    def patch(self,request):
        try:
            data            = json.loads(request.body)
            user            = request.user
            cart            = Cart.objects.get(id=data["cart_id"], user=user)
            quantity        = data["quantity"]

            if quantity <= 0:
                return JsonResponse({'message' : 'DOEDNOTEXIST_MINUS'}, status=400)
            
            cart.quantity = quantity
            cart.save()

            return JsonResponse({"MESSAGE": "PATCH_SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status=400)

        except Cart.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOESNOTEXIST_CART"}, status=400)
