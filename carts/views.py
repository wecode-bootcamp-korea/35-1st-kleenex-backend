import json

from django.db import transaction
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
            "is_checked"    : False
        } for cart in cart_list]

        return JsonResponse({'MESSAGE': result}, status=200)

    @login_decorator
    @transaction.atomic()
    def post(self, request):
        try:
            datas           = json.loads(request.body)
            user            = request.user
            product_id      = datas["product_id"]
            products        = datas["product"]
            target_product  = Product.objects.get(id = product_id)
            
            for product in products:
                quantity    = product["quantity"]
                graind      = target_product.graindbyproduct_set.get(grainding_id = product["graind"]).grainding
                size        = target_product.size_set.get(name = product["size"])

                cart, is_bool   = Cart.objects.get_or_create(
                    user        = user,
                    product     = target_product,
                    graind      = graind,
                    size        = size,
                    defaults    = {'quantity': quantity}
                )

                if not is_bool :
                    cart.quantity += quantity
                    cart.save()

            return JsonResponse({"MESSAGE": "TEST"}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEYERROR"}, status=400)

        except Size.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOESNOTEXIST_SIZE"}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOESNOTEXIST_PRODUCT"}, status=400)

        except Grainding.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOESNOTEXIST_GRAINDING"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse

        except GraindByProduct.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOESNOTEXIST_GRAINDING"}, status=400)

    @login_decorator
    def patch(self,request):
        try:
            data            = json.loads(request.body)
            user            = request.user
            cart            = Cart.objects.get(id=data["cart_id"], user=user)
            quantity        = data["quantity"]

            if quantity <= 0:
                return JsonResponse({'MESSAGE' : f'INVALID VALUE : {quantity} '}, status=400)
            
            cart.quantity = quantity
            cart.save()

            return JsonResponse({"MESSAGE": "PATCH_SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status=400)

        except Cart.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOESNOTEXIST_CART"}, status=400)

    @login_decorator
    def delete(self, request):
        try:
            datas = json.loads(request.body)
            user = request.user 
            if datas.get("is_bool"):
                Cart.objects.filter(user=user).delete()

            elif datas.get("cart_id"):
                for data in datas["cart_id"]:
                    Cart.objects.get(id=data, user=user).delete()

            return JsonResponse({"MESSAGE": "DELETE_SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

        except Cart.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOESNOTEXIST_CART"}, status=400)