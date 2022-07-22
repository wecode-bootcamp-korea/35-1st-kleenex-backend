import json

from django.http           import JsonResponse
from django.views          import View

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