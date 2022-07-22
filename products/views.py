import json

from django.http           import JsonResponse
from django.views          import View
from django.core.paginator import Paginator

from products.models  import Product, ProductImage, TasteByProduct


class MainProductView(View): 
    def get(self, request): 
        premiums             = Product.objects.all().order_by('-price')
        fresh_products       = Product.objects.all().order_by('-roasting_date')
        result_premium       = []
        result_fresh_product = []
        
        for premium in premiums[:3]: 
            images = ProductImage.objects.filter(product_id = premium.id)
            flavors  = TasteByProduct.objects.filter(product_id = premium.id)
            result_premium.append(
                {
                    'name'          : premium.name,
                    'eng_name'      : premium.eng_name,
                    'img'           : [image.url for image in images],
                    'roasting_date' : premium.roasting_date,
                    'taste'         : [flavor.taste.name for flavor in flavors],
                    'price'         : premium.price
                }
            )
        
        for fresh_product in fresh_products[:4]:
            images = ProductImage.objects.filter(product_id = fresh_product.id)
            flavors = TasteByProduct.objects.filter(product_id = fresh_product.id)
            result_fresh_product.append(
                {
                    'name'          : fresh_product.name,
                    'eng_name'      : fresh_product.eng_name,
                    'img'           : [image.url for image in images],
                    'roasting_date' : fresh_product.roasting_date,
                    'taste'         : [flavor.taste.name for flavor in flavors],
                    'price'         : fresh_product.price
                }
            )
        
        return JsonResponse({'premium' : result_premium,'fresh_product' : result_fresh_product}, status = 200)


class CoffeeProductView(View):
    def get(self, request, coffee_category_id=None):
        result_products = []
        
        if coffee_category_id == None:
            products      = Product.objects.all()
            paginator     = Paginator(products, 12)
            page_number   = request.GET.get('page')
            page_products = paginator.get_page(page_number)
        
        else:
            products      = Product.objects.filter(subcategory_id = coffee_category_id)
            paginator     = Paginator(products, 12)
            page_number   = request.GET.get('page')
            page_products = paginator.get_page(page_number)
        
        for product in page_products.object_list:
            images = ProductImage.objects.filter(product_id=product.id)
            flavors = TasteByProduct.objects.filter(product_id = product.id)
            result_products.append(
                {
                    'name'         : product.name,
                    'eng_name'     : product.eng_name,
                    'img'          : [image.url for image in images],
                    'taste'        : [flavor.taste.name for flavor in flavors],
                    'roasting_date': product.roasting_date,
                    'price'        : product.price
                }
            )
            
        return JsonResponse(
            {'shop_product_list'   : result_products},
            status = 200
        )