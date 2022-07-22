import json

from django.http           import JsonResponse
from django.views          import View

from products.models  import Grainding, Product, ProductImage, Size, TasteByProduct


class ProductDetailView(View): 
    def get(self, request, product_id): 
        product        = Product.objects.get(id=product_id)
        flavors         = TasteByProduct.objects.filter(product_id = product.id)
        grainding      = Grainding.objects.all()
        sizes          = Size.objects.all()
        product_images = ProductImage.objects.filter(product_id = product.id)
        product_detail = (
            {
                'img'        : [image.url for image in product_images],
                'name'       : product.name,
                'price'      : product.price,
                'tastes'     : [flavor.taste.name for flavor in flavors],
                'graind_type': [graind.type for graind in grainding],
                'size_type'  : [size.name for size in sizes]
            }
        )
        return JsonResponse({'product_detial' : product_detail}, status = 200)