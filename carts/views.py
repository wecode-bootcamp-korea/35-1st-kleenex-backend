import json

from django.db import transaction
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
            user            = request.user
            product_id      = datas["product_id"]
            products        = datas["product"]
            target_product  = Product.objects.get(id = product_id)

            with transaction.atomic():
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

                    if is_bool == False:
                        cart.quantity = cart.quantity + quantity
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