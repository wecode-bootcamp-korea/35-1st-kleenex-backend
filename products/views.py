import json

from django.http           import JsonResponse
from django.views          import View
from django.core.paginator import Paginator

from products.models       import Product, ProductImage, TasteByProduct

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