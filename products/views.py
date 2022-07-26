import json

from django.http           import JsonResponse
from django.views          import View

from products.models  import Product, ProductImage, TasteByProduct

from urllib.parse import unquote


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
                    } for image in ProductImage.objects.filter(product_id = premium.id)],
                    'roasting_date'  : premium.roasting_date,
                    'taste'          : [{
                        'taste_id'   : flavor.taste.id,
                        'taste_name' : flavor.taste.name
                    } for flavor in TasteByProduct.objects.filter(product_id = premium.id)],
                    'price'          : premium.price
                } for premium in premiums]
        
        result_fresh_product = [{
                    'id'             : fresh_product.id,
                    'name'           : fresh_product.name,
                    'eng_name'       : fresh_product.eng_name,
                    'img'            : [{
                        'img_id'     : image.id,
                        'img_url'    : image.url
                    } for image in ProductImage.objects.filter(product_id = fresh_product.id)],
                    'roasting_date'  : fresh_product.roasting_date,
                    'taste'          : [{
                        'taste_id'   : flavor.taste.id,
                        'taste_name' : flavor.taste.name
                    } for flavor in TasteByProduct.objects.filter(product_id = fresh_product.id)],
                    'price'          : fresh_product.price
                } for fresh_product in fresh_products]

        return JsonResponse({'premium' : result_premium,'fresh_product' : result_fresh_product}, status = 200)


class CoffeeProductView(View):
    def get(self, request):
        try:
            page             = int(request.GET.get('page')or 1)
            category         = request.GET.get('category')
            tastes           = request.GET.getlist('taste')
            filter           = request.GET.getlist('filter')
            page_size        = 12
            limit            = page_size * page
            offset           = limit - page_size
    

            products         = Product.objects.all().order_by('id')
        
            if category:
                products     = Product.objects.filter(subcategory_id=category).order_by('id')
            
            if tastes:
                products     = products.filter(taste__name__in=tastes).order_by('id').distinct()
            
            if filter:
                if 'Highprice' in filter:
                    products = products.order_by('-price')
                    if 'Highprice' in filter and 'roast' in filter:
                        products = products.order_by('-roasting_date')
                elif 'Lowprice' in filter:
                    products = products.order_by('price')
                    if 'Lowprice' in filter and 'roast' in filter:
                        products = products.order_by('-roasting_date')
                elif 'roast' in filter:
                    products = products.order_by('-roasting_date')
            
            total    = len(products)
            
            products = products[offset:limit]

            result_products = [{
                        'id'           : product.id,
                        'name'         : product.name,
                        'eng_name'     : product.eng_name,
                        'img'            : [{
                            'img_id'     : image.id,
                            'img_url'    : image.url
                        } for image in ProductImage.objects.filter(product_id = product.id)],
                        'taste'          : [{
                            'taste_id'   : flavor.taste.id,
                            'taste_name' : flavor.taste.name
                        } for flavor in TasteByProduct.objects.filter(product_id = product.id)],
                        'roasting_date': product.roasting_date,
                        'price'        : product.price
                    }for product in products]

                
            return JsonResponse(
                {'total': total, 'shop_product_list'   : result_products},
                status = 200
            )
        except ValueError:
            return JsonResponse(
                {'MESSAGE' : 'Check parameter'},
                status = 400
            )



class MainSearchView(View):
    def get(self, request):
        search = request.GET.get('search')
        key = unquote(search)
        products = Product.objects.filter(name__icontains=key)

        result = [{  
                    'id'             : product.id,
                    'name'           : product.name,
                    'eng_name'       : product.eng_name,
                    'img'            : [{
                        'img_id'     : image.id,
                        'img_url'    : image.url
                    } for image in ProductImage.objects.filter(product_id = product.id)],
                    'taste'          : [{
                        'taste_id'   : flavor.taste.id,
                        'taste_name' : flavor.taste.name
                    } for flavor in TasteByProduct.objects.filter(product_id = product.id)],
                    'roasting_date'  : product.roasting_date,
                    'price'          : product.price
                }for product in products]


        return JsonResponse({'MESSAGE' : result}, status =200)