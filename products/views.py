from itertools import count
import json

from django.http           import JsonResponse
from django.views          import View
from django.db.models      import Q

from products.models       import Product, ProductImage, TasteByProduct, Grainding, Size

from urllib.parse          import unquote


class MainProductView(View):
    def get(self, request): 
        premiums             = Product.objects.all().order_by('-price')[:3]
        fresh_products       = Product.objects.all().order_by('-roasting_date')[:4]
        result_premium       = [{
                    'id'             : premium.id,
                    'name'           : premium.name,
                    'eng_name'       : premium.eng_name,
                    'img'            : [{
                        'img_id'     : image.id,
                        'img_url'    : image.url
                    } for image in premium.productimage_set.all()],
                    'roasting_date'  : premium.roasting_date,
                    'taste'          : [{
                        'taste_id'   : flavor.taste.id,
                        'taste_name' : flavor.taste.name
                    } for flavor in premium.tastebyproduct_set.all()],
                    'price'          : premium.price
                } for premium in premiums]
        
        result_fresh_product = [{
                    'id'             : fresh_product.id,
                    'name'           : fresh_product.name,
                    'eng_name'       : fresh_product.eng_name,
                    'img'            : [{
                        'img_id'     : image.id,
                        'img_url'    : image.url
                    } for image in fresh_product.productimage_set.all()],
                    'roasting_date'  : fresh_product.roasting_date,
                    'taste'          : [{
                        'taste_id'   : flavor.taste.id,
                        'taste_name' : flavor.taste.name
                    } for flavor in fresh_product.tastebyproduct_set.all()],
                    'price'          : fresh_product.price
                } for fresh_product in fresh_products]

        return JsonResponse({'premium' : result_premium,'fresh_product' : result_fresh_product}, status = 200)


class CoffeeProductView(View):
    def get(self, request):      
        category         = request.GET.get('category')
        tastes           = request.GET.getlist('taste')
        sorting          = request.GET.get('sorting')
        offset           = int(request.GET.get('offset', 0))
        limit            = int(request.GET.get('limit', 12))

        q = Q()

        if category:
            q &= Q(subcategory_id = category)
        
        if tastes:
            q &= Q(taste__name__in = tastes)

        sort_dict = {
        'Highprice' : '-price',
        'Lowprice'  : 'price',
        'roast'     : '-roasting_date',
        None        : 'id'
        }
        
        total = Product.objects.all().count()

        products = Product.objects.filter(q).order_by(sort_dict.get(sorting)).distinct()[offset:offset+limit]

        result_products = [{
                    'id'             : product.id,
                    'name'           : product.name,
                    'eng_name'       : product.eng_name,
                    'img'            : [{
                        'img_id'     : image.id,
                        'img_url'    : image.url
                    } for image in product.productimage_set.all()],
                    'taste'          : [{
                        'taste_id'   : flavor.taste.id,
                        'taste_name' : flavor.taste.name
                    } for flavor in product.tastebyproduct_set.all()],
                    'roasting_date'  : product.roasting_date,
                    'price'          : product.price
                }for product in products]

        return JsonResponse(
            {
            'total' : total,
            'shop_product_list'   : result_products
            },
            status = 200
        )


class ProductDetailView(View): 
    def get(self, request, product_id): 
        try:

            product        = Product.objects.get(id=product_id)

            product_detail = (
                {
                    'id'               : product.id,
                    'name'             : product.name,
                    'price'            : product.price,
                    'img'              : [{
                        'img_id'       : image.id,
                        'img_url'      : image.url
                    } for image in product.productimage_set.all()],

                    'taste'            : [{
                        'taste_id'     : flavor.taste.id,
                        'taste_name'   : flavor.taste.name
                    } for flavor in product.tastebyproduct_set.all()],
                    'graind'           : [{
                        'graind_id'    : graind.id,
                        'graind_type'  : graind.type
                    } for graind in product.grainding_set.all()],
                    'size'             : [{
                        'size_id'      : size.id,
                        'size_name'    : size.name,
                        'size_price'   : size.price
                    } for size in product.size_set.all()],
                }
            )
            return JsonResponse({'product_detail' : product_detail}, status = 200)

        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'Product matching query does not exist.'}, status = 404)


class MainSearchView(View):
    def get(self, request):
        search = request.GET.get('keywords')
        products = Product.objects.filter(name__icontains=unquote(search))

        result = [{  
                    'id'             : product.id,
                    'name'           : product.name,
                    'eng_name'       : product.eng_name,
                    'img'            : [{
                        'img_id'     : image.id,
                        'img_url'    : image.url
                    } for image in product.productimage_set.all()],
                    'taste'          : [{
                        'taste_id'   : flavor.taste.id,
                        'taste_name' : flavor.taste.name
                    } for flavor in product.tastebyproduct_set.all()],
                    'roasting_date'  : product.roasting_date,
                    'price'          : product.price
                }for product in products]

        if len(products) == 0:
            return JsonResponse({'MESSAGE' : 'NO RESULT'}, status=404)

        return JsonResponse({'result' : result}, status =200)


class MainSearchView(View):
    def get(self, request):
        search   = request.GET.get('keywords')
        products = Product.objects.filter(name__icontains=unquote(search))

        result = [{  
                    'id'             : product.id,
                    'name'           : product.name,
                    'eng_name'       : product.eng_name,
                    'img'            : [{
                        'img_id'     : image.id,
                        'img_url'    : image.url
                    } for image in product.productimage_set.all()],
                    'taste'          : [{
                        'taste_id'   : flavor.taste.id,
                        'taste_name' : flavor.taste.name
                    } for flavor in product.tastebyproduct_set.all()],
                    'roasting_date'  : product.roasting_date,
                    'price'          : product.price
                }for product in products]

        if not products.exists():
            return JsonResponse({'MESSAGE' : 'NO RESULT'}, status=404)

        return JsonResponse({'result' : result}, status =200)