import json

from django.http import JsonResponse
from django.views import View

from carts.models import Cart
from products.models import *
from core.utils import login_decorator

class CartView(View):
    @login_decorator
    def delete(self, request):
        try:
            datas = json.loads(request.body)

            if "is_bool" in datas and datas["is_bool"] == "True" :
                Cart.objects.all().delete()

            elif "is_bool" not in datas and "cart_id" in datas:
                for data in datas["cart_id"]:
                    Cart.objects.get(id = data).delete()

            return JsonResponse({"MESSAGE": "DELETE_SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status=400)

        except Cart.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOESNOTEXIST_CART"}, status=400)