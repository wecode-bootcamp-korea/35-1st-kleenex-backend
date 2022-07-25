import json

from django.http           import JsonResponse
from django.views          import View

from products.models  import Product, ProductImage, TasteByProduct


class MainProductView(View): 
    def get(self, request): 
        premiums             = Product.objects.all().order_by('-price')[:3]
        fresh_products       = Product.objects.all().order_by('-roasting_date')[:4]

        result_premium       = [{
                    'id'            : premium.id,
                    'name'          : premium.name,
                    'eng_name'      : premium.eng_name,
                    'img'           : [image.url for image in ProductImage.objects.filter(product_id = premium.id)],
                    'img_id'        : [image.id for image in ProductImage.objects.filter(product_id = premium.id)],
                    'roasting_date' : premium.roasting_date,
                    'taste'         : [flavor.taste.name for flavor in TasteByProduct.objects.filter(product_id = premium.id)],
                    'taste_id'      : [flavor.taste.id for flavor in TasteByProduct.objects.filter(product_id = premium.id)],
                    'price'         : premium.price
                } for premium in premiums]
        
        result_fresh_product = [{
                    'id'            : fresh_product.id,
                    'name'          : fresh_product.name,
                    'eng_name'      : fresh_product.eng_name,
                    'img'           : [image.url for image in ProductImage.objects.filter(product_id = fresh_product.id)],
                    'img_id'        : [image.id for image in ProductImage.objects.filter(product_id = fresh_product.id)],
                    'roasting_date' : fresh_product.roasting_date,
                    'taste'         : [flavor.taste.name for flavor in TasteByProduct.objects.filter(product_id = fresh_product.id)],
                    'taste_id'      : [flavor.taste.id for flavor in TasteByProduct.objects.filter(product_id = fresh_product.id)],
                    'price'         : fresh_product.price
                } for fresh_product in fresh_products]

        return JsonResponse({'premium' : result_premium,'fresh_product' : result_fresh_product}, status = 200)