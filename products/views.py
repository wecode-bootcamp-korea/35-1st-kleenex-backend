import json

from django.http           import JsonResponse
from django.views          import View
from django.db.models      import Q

from products.models  import Product, ProductImage, TasteByProduct, Grainding, Size


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
        """
        python dictionary
        dict = {
            a : 1,
            b : 2, 
            c : 3
        }

        dict['d'] // raise KeyError
        dict.get('d') // 
        """
        category         = request.GET.get('category')
        tastes           = request.GET.getlist('taste')
        sorting          = request.GET.get('sorting', 'id')
        offset           = int(request.GET.get('offset', 0))
        limit            = int(request.GET.get('limin', 9))

        # products         = Product.objects.all().order_by('id')
    
        # if category:
        #     products     = Product.objects.filter(subcategory_id=category).order_by('id')
        
        # if tastes:
        #     products     = products.filter(taste__name__in=tastes).order_by('id').distinct()

        q = Q()

        if category:
            q &= Q(subcategory_id=category)

        if tastes:
            q &= Q(taste__name__in=tastes)

        sort_dict = {
            'Highprice' : '-price',
            'Lowprice'  : 'price',
            'roast'     : '-roasting_date',
            'id'        : 'id'
        }

        products = Product.objects.filter(q).order_by(sort_dict.get(sorting))[offset:offset+limit]

        
        # if filter:
        #     if 'Highprice' in filter:
        #         products = products.order_by('-price')
        #     elif 'Lowprice' in filter:
        #         products = products.order_by('price')
        #     elif 'roast' in filter:
        #         products = products.order_by('-roasting_date')

        result_products = [{
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

        return JsonResponse(
            {
                'total'             : len(products), 
                'shop_product_list' : result_products
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
                    } for image in ProductImage.objects.filter(product_id = product.id)],

                    'taste'            : [{
                        'taste_id'     : flavor.taste.id,
                        'taste_name'   : flavor.taste.name
                    } for flavor in TasteByProduct.objects.filter(product_id = product.id)],
                    'graind'           : [{
                        'graind_id'    : graind.id,
                        'graind_type'  : graind.type
                    } for graind in Grainding.objects.all()],
                    'size'             : [{
                        'size_id'      : size.id,
                        'size_name'    : size.name,
                        'size_price'   : size.price
                    } for size in Size.objects.filter(product_id = product.id)],
                }
            )
            return JsonResponse({'product_detail' : product_detail}, status = 200)

        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'Product matching query does not exist.'}, status = 404)
            

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
                    } for image in ProductImage.objects.filter(product_id = product.id)],
                    'taste'          : [{
                        'taste_id'   : flavor.taste.id,
                        'taste_name' : flavor.taste.name
                    } for flavor in TasteByProduct.objects.filter(product_id = product.id)],
                    'roasting_date'  : product.roasting_date,
                    'price'          : product.price
                }for product in products]

        if len(products) == 0:
            return JsonResponse({'MESSAGE' : 'NO RESULT'}, status=404)

        return JsonResponse({'result' : result}, status =200)
