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

            for data in datas:
                product = Product.objects.get(id=datas[data]["id"])
                datas[data]['quantity']
                product.graindbyproduct_set.get(grainding_id=datas[data]['graind']).grainding
                product.size_set.get(name=datas[data]['size'])

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
            for data in datas:
                user            = request.user
                product         = Product.objects.get(id = datas[data]["id"])
                quantity        = datas[data]['quantity']
                graind          = product.graindbyproduct_set.get(grainding_id=datas[data]['graind']).grainding
                size            = product.size_set.get(name=datas[data]['size'])
                curr_cart_bool  = Cart.objects.filter(user=user.id, product=product.id, graind=graind.id, size=size.id)

                if curr_cart_bool.exists():
                    curr_cart           = Cart.objects.get(user=user.id, product=product.id, graind=graind.id, size=size.id)
                    curr_cart.quantity  = curr_cart.quantity + quantity
                    curr_cart.save()
                else:
                    Cart.objects.create(user=user,product = product, graind=graind, size=size, quantity=quantity)

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)