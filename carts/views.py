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
            targe_product   = Product.objects.get(id = product_id)

            for product in products:
                targe_product.graindbyproduct_set.get(grainding_id = product["graind"]).grainding
                targe_product.size_set.get(name = product["size"])

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

        except Size.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOESNOTEXIST_SIZE"}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOESNOTEXIST_PRODUCT"}, status=400)

        except Grainding.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOESNOTEXIST_GRAINDING"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE": "JSONDECODE_ERROR"}, status=400)

        except GraindByProduct.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOESNOTEXIST_GRAINDING"}, status=400)

        else:
            for product in products:
                user                = request.user
                origin_product      = Product.objects.get(id = product_id)
                quantity            = product["quantity"]
                graind              = origin_product.graindbyproduct_set.get(grainding_id = product["graind"]).grainding
                size                = origin_product.size_set.get(name = product["size"])

                cart, is_bool       = Cart.objects.get_or_create(
                        user        =   user,
                        product     =   origin_product,
                        graind      =   graind,
                        size        =   size,
                        defaults    =   {'quantity' : quantity}
                )

                if not is_bool:
                    cart.quantity += quantity
                    cart.save()

            return JsonResponse({"MESSAGE": "TEST"}, status=200)