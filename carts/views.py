import json

from django.http import JsonResponse
from django.views import View

from carts.models import Cart
from products.models import *
from core.utils import login_decorator

class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            datas           = json.loads(request.body)
            product_id      = datas["product_id"]
            products        = datas["product"]
            add_product  = Product.objects.get(id=product_id)

            for product in products:
                add_product.graindbyproduct_set.get(grainding_id=product["graind"]).grainding
                add_product.size_set.get(name=product["size"])

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

        else:
            for product in products:
                user                = request.user
                origin_product      = Product.objects.get(id=product_id)
                quantity            = product["quantity"]
                graind              = origin_product.graindbyproduct_set.get(grainding_id=product["graind"]).grainding
                size                = origin_product.size_set.get(name=product["size"])
                curr_cart_bool      = Cart.objects.filter(user=user.id, product=origin_product.id, graind=graind.id, size= size.id)

                if curr_cart_bool.exists():
                    curr_cart           = Cart.objects.get(user=user.id, product=origin_product.id, graind=graind.id, size= size.id)
                    curr_cart.quantity  = curr_cart.quantity + quantity
                    curr_cart.save()
                else:
                    Cart.objects.create(user=user, product=origin_product, graind=graind, size=size, quantity=quantity)

            return JsonResponse({"MESSAGE": "TEST"}, status=200)
