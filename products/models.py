from django.db import models

from core.models import TimeStampModel


class Category(models.Model): 
    name               = models.CharField(max_length=50)

    class Meta:
        db_table       = 'categories'



class SubCategory(models.Model): 
    name               = models.CharField(max_length = 50)
    category           = models.ForeignKey('Category', on_delete = models.CASCADE)

    class Meta:
        db_table       = 'subcategories'


class Product(TimeStampModel):
    name               = models.CharField(max_length = 150, unique = True)
    eng_name           = models.CharField(max_length = 250, unique = True)
    roasting_date      = models.DateField()
    price              = models.DecimalField(max_digits = 8, decimal_places = 2)
    subcategory        = models.ForeignKey('Subcategory', on_delete=models.CASCADE)

    class Meta:
        db_table       = 'products'


class ProductImage(models.Model):
    url                = models.CharField(max_length = 300)
    product            = models.ForeignKey('Product', on_delete = models.CASCADE)

    class Meta:
        db_table       = 'product_images'


class Size(models.Model): 
    name               = models.CharField(max_length = 50)
    price              = models.DecimalField(max_digits = 8, decimal_places = 2)
    product            = models.ForeignKey('Product', on_delete = models.CASCADE)
  
    class Meta:
        db_table       = 'sizes'
  

class Taste(models.Model): 
    name               = models.CharField(max_length = 50)
    products_tastes    = models.ManyToManyField(
        'Product',
        through        = 'TasteByProduct',
        through_fields = ('taste', 'product')
    )

    class Meta:
        db_table       = 'tastes'


class TasteByProduct(models.Model): 
    product            = models.ForeignKey('Product', on_delete = models.CASCADE)
    taste              = models.ForeignKey('Taste',   on_delete = models.CASCADE)

    class Meta: 
        db_table       = 'taste_by_products'

class Grainding(models.Model): 
    type               = models.CharField(max_length = 100)
    products_grainding = models.ManyToManyField(
        'Product',
        through        = 'GraindByProduct',
        through_fields = ('grainding', 'product')
    )

    class Meta: 
        db_table       = 'graindings'


class GraindByProduct(models.Model): 
    product            = models.ForeignKey('Product',   on_delete = models.CASCADE)
    grainding          = models.ForeignKey('Grainding', on_delete = models.CASCADE)

    class Meta: 
        db_table       = 'grainding_by_products'